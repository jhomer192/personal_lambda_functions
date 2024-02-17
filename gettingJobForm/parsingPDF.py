import pdfplumber
import re


def process_box(dict, text):
    split_string = re.split(r'[:\n]', text)
    if len(split_string) == 2:
        dict[split_string[0]] = split_string[1]
    elif len(split_string) > 2:
        dict["header"] = split_string
        
    
def get_dict_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
   
        cur_form_data = {}
        cur_form_data["form title"] = pdf.pages[0].extract_text().split("\n")[0]
        first = True
        for page in pdf.pages:
            if not first:
                process_box(cur_form_data, page.extract_text().split("\n")[0])
            
            tables = page.extract_tables()
            first = False
            for table in tables:
                for row in table:
                    process_box(cur_form_data, row[0])

    # Close the PDF file
    pdf.close()
    return cur_form_data
