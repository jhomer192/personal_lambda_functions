import pdfplumber
import re

def get_month_from_day(month):
    if month == "January":
        return "01"
    elif month == "February":
        return "02"
    elif month == "March":
        return "03"
    elif month == "April":
        return "04"
    elif month == "May":
        return "05"
    elif month == "June":
        return "06"
    elif month == "July":
        return "07"
    elif month == "August":
        return "08"
    elif month == "September":
        return "09"
    elif month == "October":
        return "10"
    elif month == "November":
        return "11"
    elif month == "December":
        return "12"
    else:
        return "Invalid month"
def add_0(day):
    if len(day) == 1:
        return "0" + day
    else:
        return day

def process_box(dict, text):
    split_string = re.split(r'[:\n]', text)
    if len(split_string) == 2:
        dict[split_string[0]] = split_string[1]
    elif len(split_string) > 2:
        name_split = split_string[0].split(" ")
        dict['#'] = int(split_string[1][1:])
        dict["First name"] = name_split[0]
        dict["Last name"] = name_split[1]
        raw_date = split_string[2].split(" ")
        dict["Submission Date"] = get_month_from_day(raw_date[0]) + "/" + add_0(raw_date[1].replace(",", "")) + "/" + raw_date[2].replace(",", "")
        dict["Submission Time"] = raw_date[3] + ":" + split_string[3][:5]
        
    
def get_dict_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
   
        cur_form_data = {}
        cur_form_data["client"] = pdf.pages[0].extract_text().split("\n")[0].split(" ")[0]
        first = True
        for page in pdf.pages:
            if not first:
                process_box(cur_form_data, page.extract_text().split("\n")[0])
            
            tables = page.extract_tables()
            text = page.extract_text()
            splitText = text.split("\n")
            if splitText is not {}:
                if "What model is the" in splitText[0]: #making sure first item on each page is added is what model doens't work
                    process_box(cur_form_data, splitText[0]+ ":" + splitText[1])
                else:
                    process_box(cur_form_data, splitText[0])
                if not tables:
                    for item in text.split("\n"):
                        process_box(cur_form_data, item)
            first = False
            for table in tables:
                for row in table:
                    process_box(cur_form_data, row[0])

    # Close the PDF file
    pdf.close()
    return cur_form_data
