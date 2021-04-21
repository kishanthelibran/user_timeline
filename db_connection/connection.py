import psycopg2
from db_connection.config import config as config
def get_query_response(query):
    conn=None
    cursor=None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    finally:
        if cursor !=None:
            cursor.close()
        if conn !=None:
            conn.close()
    return data
def get_update_response(query):
    conn=None
    cursor=None
    f=False
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        f=True
    finally:
        if cursor !=None:
            cursor.close()
        if conn !=None:
            conn.close()
    return f
def get_insert(query,recordlist):
    conn=None
    cursor=None
    f=False
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        cursor.execute(query,recordlist)
        conn.commit()
        f=True
    finally:
        if cursor !=None:
            cursor.close()
        if conn !=None:
            conn.close()
    return f

#query="select * from user_details"
#k=get_query_response(query)
#print(k)
'''USER_NAME='so'
USER_EMAIL='ABcd@GMAIL.COM'
MOBILE_NO='8974824340'
USER_LOCATION='chennaiex'
PASSWORD='1234'
query2="INSERT INTO user_details(user_name,user_email,mobile_no,user_location,password) VALUES (%s,%s,%s,%s,%s)"
record=(USER_NAME,USER_EMAIL,MOBILE_NO,USER_LOCATION,PASSWORD)
mm=get_insert(query2,record)
print(mm)'''