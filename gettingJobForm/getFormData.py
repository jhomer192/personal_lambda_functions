import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import tempfile
import os
import parsingPDF
import parsingHTMShift
import shutil
from bs4 import BeautifulSoup
# Outlook.com IMAP server settings
IMAP_SERVER = 'outlook.office365.com'
IMAP_PORT = 993
EMAIL = 'ohmev@outlook.com'
PASSWORD = '8eGK6nT!vcs!KZL@'
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USERNAME = EMAIL
SMTP_PASSWORD = PASSWORD


def get_pdf_from_email(filename, part):
    attachment_data = part.get_payload(decode=True)
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, filename)
    with open(save_path, 'wb') as f:
            f.write(attachment_data)
    # Return the parsed PDF data
    to_return = parsingPDF.get_dict_from_pdf(save_path)
    shutil.rmtree(temp_dir)
    return to_return

def forward_email(message, reciepent):
    forward_message = MIMEMultipart()
    forward_message['From'] = EMAIL
    forward_message['To'] = reciepent
    forward_message['Subject'] = 'Fwd: ' + message['Subject']
    payload = message.get_payload(decode=True)
    if payload is not None:
        forward_message.attach(MIMEText(payload, 'plain')) # attach original text message
    for part in message.walk(): #attaching attachments on original message
        if part.get_content_maintype() == 'multipart':
            continue
        attachment = MIMEBase(part.get_content_type(), part.get_content_subtype())
        attachment.set_payload(part.get_payload(decode=True))
        encoders.encode_base64(attachment)
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                ext = '.bin'
            filename = f'attachment{ext}'
        attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        forward_message.attach(attachment)
    
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp_server.sendmail(EMAIL, reciepent, forward_message.as_string())
    smtp_server.quit()

def singular_email(imap_server, emailid, clientData, shiftData, shiftIDs):
    
    status, data = imap_server.fetch(emailid, '(RFC822)')
    raw_email = data[0][1]
    message = email.message_from_bytes(raw_email)
    #get_pdf_from_email
    # print(f"parsing for right location with {message["From"]} and {message["Subject"]}")
    if message['From'] == 'OhmEV App <noreply@reports.connecteam.com>': #form report
        # print("found report related email")
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            filename = part.get_filename()
            if filename and ".pdf" in filename:
                dictToSpawn = get_pdf_from_email(filename, part)
                if dictToSpawn["client"] in clientData:
                    clientData[dictToSpawn["client"]].append(dictToSpawn)
                else:
                    clientData[dictToSpawn["client"]] = [dictToSpawn]
    elif message['From'] == 'Connecteam <noreply@connecteam.com>' and " shift " in message["Subject"]:
        # print("found shift related email")
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" not in content_disposition:
                # Content type should be text/plain or text/html
                if content_type == "text/html":
                    # Convert HTML to plain text
                    soup = BeautifulSoup(part.get_payload(decode=True).decode(), 'html.parser')
                    
                    shift_op_to_add = parsingHTMShift.get_singular_shift_dict(soup.get_text(), message["Subject"], message["Date"])
                    if shift_op_to_add is not None: #WILL NOT GET READ IF SHIFT EMAILS DON'T CONTAIN LEVEL
                        if shift_op_to_add["ticketID"] in shiftIDs:
                            index_to_remove = None
                            for i, d in enumerate(shiftData):
                                if d.get("ticketID") == shift_op_to_add["ticketID"]:
                                    index_to_remove = i
                                    break
                            if index_to_remove is not None:
                                del shiftData[index_to_remove]
                        else: 
                            shiftIDs.append(shift_op_to_add["ticketID"])
                        shiftData.append(shift_op_to_add)
    
def process_emails(event, context):
    imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap_server.login(EMAIL, PASSWORD)
    imap_server.select('INBOX')
    clientData = {}
    shiftData = []
    shiftIDs = []
    status, messages = imap_server.search(None, 'UNSEEN')
    if status == 'OK':
        emailids = messages[0].split()

        for emailid in emailids:
            singular_email(imap_server, emailid, clientData, shiftData, shiftIDs)
            
            
                        #Now that we have a raw dict signal another service to handle it

            # forward_email(message, 'jack@ohmev.net')
           
    #         imap_server.store(emailid, '+FLAGS', '\\Deleted');  #marks email for deletion
    # imap_server.expunge(); #deletes all marked for deletion
    imap_server.logout()
    return {"inspections":clientData, "shift_indicators":shiftData}
print(process_emails(5,5))