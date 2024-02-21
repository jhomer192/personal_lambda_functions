
def get_singular_shift_dict(plainTextHTML, subject):
    if "Level2" in plainTextHTML: #ensuring it is a level2 
        if " accepted " in subject: #accept
            toAdd = {}
            split_subject = subject.split(" ")
            toAdd["operation"] = "accepted"
            toAdd["First"] = split_subject[0]
            toAdd["Last"] = split_subject[1]
            for line in plainTextHTML.splitlines():
                if "Level2" not in line:
                    continue
                split_line = line.split(" ")
                toAdd["job_type"] = split_line[0] + " " + split_line[1]
                toAdd["ticketID"] = split_line[-1]
                break
            if toAdd:
                return toAdd

        elif " completed " in subject: #completed
            toAdd = {}
            split_subject = subject.split(" ")
            toAdd["operation"] = "completed"
            toAdd["First"] = split_subject[0]
            toAdd["Last"] = split_subject[1]
            for line in plainTextHTML.splitlines():
                if "Level2" not in line:
                    continue
                split_line = line.split(" ")
                toAdd["job_type"] = split_line[0] + " " + split_line[1]
                toAdd["ticketID"] = split_line[-1]
                break
            if toAdd:
                return toAdd
    return {}