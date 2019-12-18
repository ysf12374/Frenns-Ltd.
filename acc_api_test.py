import numpy as np
# import pandas as pd
import mysql.connector
import config
import json
import datetime
mysql = mysql.connector.connect(
  host=config.HOST,
  user=config.USER,
  passwd=config.PSWD,
  database = config.FRENNS_NAME5)
req={"customer_id":"FRN100000647"}
cur=mysql.cursor()
frenns_id='FRN100000647'
cur.execute("SELECT * FROM syncfraudanalysis WHERE syncfraudanalysis.frenns_id='"+str(frenns_id)+"'")
update=cur.fetchall()
# cur.execute("SELECT datetime,date_from, date_to FROM syncfraudanalysis WHERE syncfraudanalysis.frenns_id='"+str(frenns_id)+"'")
# update1=cur.fetchall()
def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()
 
status1=json.dumps(update, default = myconverter)
# print(status1)
# status2=json.dumps(update)
# print(status2)
# status={"first":status1,"second":status2}
status3=status1
# from jsonmerge import merge
# result = merge(status1, status2)
print(status3)
cur.close()
mysql.close()