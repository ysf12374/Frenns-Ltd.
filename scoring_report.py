# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:22:30 20i9
@author: Yousuf
"""

import mysql.connector
import numpy as np
import pandas as pd
import datetime
import re
import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s')#filename='analysis.log',filmode='w'
def update(x,i,j,cn,frn):
    import mysql.connector
    import re
    import clearsight_final
    import arima_commandline_new,frennns_creditscore_cronjob,Scorebeneish,Bradford_law,beneishscore,z_score,frennns_creditscore_commandline,config

    mysql = mysql.connector.connect(
		host=config.HOST,
      	user=config.USER,
      	passwd=config.PSWD,
      	database = config.FRENNS_NAME
      )
    mycursor=mysql.cursor()
    if re.search("clearsight_final",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        cnn=str(cn[j])
        cnn=cnn.replace(' ','')
        k=clearsight_final.regnum(cnn)
        #print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors':
                k=clearsight_final.regnum(cnn)

        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='clearsight_final.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
    elif re.search("paydays_prediction",str(x)) or re.search("expense_prediction",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        k=arima_commandline_new.call(str(frn[j]),str(cn[j]))
#        print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors':
                k=arima_commandline_new.call(str(frn[j]),str(cn[j]))

        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='paydays.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
    elif re.search("scorebeneish",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        
        k=Scorebeneish.regnum(str(frn[j]))
#        print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors':
                k=Scorebeneish.regnum(str(frn[j]))
        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='beneishfrenns.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
    elif re.search("bradford_law",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        k=Bradford_law.call(str(frn[j]))
#        print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors' or k=='Manual Upload':
                k=Bradford_law.call(str(frn[j]))
        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='bradfordslaw.py'
            my_mail(nm,frn[j],cn[j],i)
        elif k=='Manual Upload':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='bradfordslaw.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
    elif re.search("beneishscore",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        cnn=str(cn[j])
        cnn=cnn.replace(' ','')
        k=beneishscore.regnum(cnn)
#        print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors':
                k=beneishscore.regnum(cnn)
        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='beneishscore.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
    elif re.search("z_score",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        k=z_score.zscore(str(frn[j]))
        #print (k)
        logging.debug(k)
        for a in range(0,4):
            if k=='Executed with some errors':
                k=z_score.zscore(str(frn[j]))
        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='z_score.py'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()    
    elif re.search("frennns_creditscore_commandline",str(x)):
        time=datetime.datetime.now()
        time=str(time)
        status=1
        records=[status]
        sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
        mycursor.execute(sql,records)
        mysql.commit()
        k=frennns_creditscore_cronjob.call(str(frn[j]),str(cn[j]))
        logging.debug(k)
        
        for a in range(0,4):
            if k=='Executed with some errors' or k=='Manual Upload':
                k=frennns_creditscore_cronjob.call(str(frn[j]),str(cn[j]))
        if k=='Executed with some errors':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='frennsid_creditscore.py'
            my_mail(nm,frn[j],cn[j],i)
        elif k=='Manual Upload':
            status=0
            records=[status]
            sql = "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='frennsid_creditscore.py < Manual Upload >'
            my_mail(nm,frn[j],cn[j],i)
        else:
            status=2
            records=[status,time]
            sql= "UPDATE scoring_script SET status=%s,completed_at=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()  
    else:
            status=0
            records=[status]
            sql= "UPDATE scoring_script SET status=%s  WHERE score_id='" + i + "'"
            mycursor.execute(sql,records)
            mysql.commit()
            nm='Didnt Update'
            my_mail(nm,frn[j],cn[j],i)
    #return k
            
def my_mail(nm,frn,cn,i):
    try:
        import smtplib
        import ssl
        import datetime
        EMAIL_ADDRESS='1111cronjobs@frenns.com'
        EMAIL_PASSWORD='1111gnK26q$6'
        print(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp_server='mail.1frenns.com'
        port=25
        subject='Please check analysis'
    #    body=' {0} and FRN {1} and company number {2} that does not seem to work'.format(nm,frn,cn,i)
        date=datetime.datetime.now()
        date=str(date)
        body="Scriptname: {0}\n  FRN {1}  \n Company number: {2} \n Run ID {3}\n Date: {4}\n".format(nm,frn,cn,i,date)
        msg='Subject: {0}\n\n{1}'.format(subject,body)
        logging.debug(msg)
        print(msg)
        #context=ssl.create_default_context()
        #server=smtplib.SMTP('smtp.yandex.com.tr:587')
        server=smtplib.SMTP('mail.frenns.com:25')
        server.starttls()
    #    server.ehlo()
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS,'it@frenns.com',msg)
        server.quit()
    except Exception as e:
        #print (e)
        logging.debug(e)
#    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
#    smtp.ehlo()
#    smtp.starttls()
#    smtp.ehlo()
#    
#    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
#
#    smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,msg)

import config        
mysql = mysql.connector.connect(
		host=config.HOST,
     	user=config.USER,
      	passwd=config.PSWD,
      	database = config.FRENNS_NAME
      )
jf=pd.read_sql('select frn,company_number,script from scoring_script', con=mysql)
script=jf['script']
cn=jf['company_number']
frn=jf['frn']
 
for j in range(0,len(script)):      
    yf=pd.read_sql("""select processed from synchronize_jobs where user_number="{0}" """.format(frn[j]), con=mysql)
    processed=yf['processed']
    import subprocess
    if processed.values==1:
        x=re.findall("[_a-z]*.py$",script[j].lower())
        i=j+1
        i=str(i)
        update(x,i,j,cn,frn)
    subprocess.call(["php", "/var/www/vhosts/vkingsolutions.com/public_html/dev/cron-mail/set_companydata_customer.php","frnId:{0}".format(frn[j])])

mysql.commit()
mysql.close()

#import subprocess
##subprocess.call("php E:\\per_PPH\\demo\\set_companydata_customer.php")
#import subprocess
#
#result = subprocess.run(
#    ['php', 'set_companydata_customer.php'],    # program and arguments
#    stdout=subprocess.PIPE,  # capture stdout
#    check=True               # raise exception if program fails
#)
#print(result.stdout)


