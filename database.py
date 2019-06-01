import settings
import mysql.connector

try:
    con = mysql.connector.connect(user=settings.MYSQL_USER, password=settings.MYSQL_PSWD,
                                  host=settings.MYSQL_HOST,
                                  database=settings.MYSQL_NAME,buffered=True,charset="utf8", use_unicode=True)
    
    cursor = con.cursor()
except Exception as e:
    print('An error occurred in database.py')
    print(e.args)
    print(e)
    

