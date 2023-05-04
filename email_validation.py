from verify_email import verify_email
from database_connection import Database_Connection
from niche_details import *
import time

def mysql_commit_query_executer(query):
    db_connection,db_cursor = Database_Connection()
    db_cursor.execute(query)
    db_connection.commit()
    db_cursor.close()
    
def mysql_fetch_query_executer(query):
    db_connection,db_cursor = Database_Connection()
    db_cursor.execute(query)
    data = db_cursor.fetchall()
    db_cursor.close()
    return data

def get_valid_email(emails):
    print("Validating Emails...")
    verify_email_list = []
    if emails:
        for email in emails:
            start_time = 0
            end_time = 0
            start_time = time.time()
            if verify_email(email,timeout=5):
                verify_email_list.append(email)
            end_time = time.time()
            print(f"Total Time Tooks : {end_time - start_time}")
        return str(verify_email_list).replace("[","").replace("]","").replace("'","")
    else:
        return None
    
def get_gl_id_and_email_from_db(data_table):
    query = f"select gl_id,email from {data_table} where gl_website is not null and gl_website !='None' and email is not null and email !='' order by rand() limit 1;"
    data = mysql_fetch_query_executer(query)
    
    return data
 
def get_email_list(data_table):
    print("Fetching Emails from db....")
    data = get_gl_id_and_email_from_db(data_table)
    gl_id = (data[0][0])
    emails = (data[0][1])
    
    if (emails.find(',')) == -1:
        emails = [emails]
    else:
        emails = emails.split(',')
    return gl_id,emails

def get_remaining_count_of_website(data_table):
    query = f"select count(*) from {data_table} where gl_website !='None' and gl_website is not null and valid_email is null and email is not null and email !='';"
    data = mysql_fetch_query_executer(query)
    # print(data)
    return data[0][0]

def update_email_to_database(gl_id,valid_email,data_table):
    query = f"""update {data_table} set valid_email = "{valid_email}" where gl_id = {gl_id}"""
    mysql_commit_query_executer(query)
    print(f"updated: {valid_email} gl_id: {gl_id}")

def main(data_table):
    remaing_emails_count =get_remaining_count_of_website(data_table)
    while remaing_emails_count > 0: 
        gl_id,emails = get_email_list(data_table)
        verify_email_list = get_valid_email(emails)
        
        if verify_email_list !='':
                update_email_to_database(gl_id,verify_email_list,data_table)
        # print(emails)
        remaing_emails_count =get_remaining_count_of_website(data_table)

if __name__ == '__main__':

    main(data_table)

