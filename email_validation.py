from verify_email import verify_email


def get_valid_email(emails):
    verify_email_list = []
    if emails:
        for email in emails:
            if verify_email(email):
                verify_email_list.append(email)
        return verify_email_list
    else:
        return None
    
def get_glid_email_from_db():
    
        



