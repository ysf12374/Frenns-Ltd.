
# def regnum(reg):  
    
    # try:
import numpy as np
# import pandas as pd
import mysql.connector
import config
from tqdm import tqdm
mysql = mysql.connector.connect(
  host=config.HOST,
  user=config.USER,
  passwd=config.PSWD,
  database = config.FRENNS_NAME5
  )
    ###########################################################################################################
    ####### These are mysql queries to select the columns from clearsight_development table  ##################
    ###########################################################################################################
        
        # df = pd.read_sql('select * from company_ann_reports where CompanyNumber = "' + reg + '"', con=mysql)

        
                
        # records=[str(reg), str(naame),str(CreditRating),str(CreditScore),creditlimits,str(revv)]#,str(combinedcreditscore),str(combinedpurchasescore)]
        
        # recds=[str(CreditRating),str(CreditScore),creditlimits,str(revv)]#,str(combinedcreditscore),str(combinedpurchasescore)]
    #################################################################################################################################
    ####  checking if the company scores already exists, if it does then update the table OR insert a new row otherwise##############
    #################################################################################################################################
        
mycursor=mysql.cursor()
mycursor.execute("SELECT syncinvoice_id,product_id FROM marketplace_mpbidding_product ")
update=mycursor.fetchall()
# print(update)
for s_id in tqdm(update):
    syncinvoice_id=s_id[0]
    auction_id=s_id[1]
    mycursor.execute("SELECT id FROM bankout_details WHERE substr(auction_id,-5,5)='"+str(auction_id)+"' ")
    ids=mycursor.fetchall()

    try:
        if ids:
            sql_update_query = "UPDATE syncinvoice set flags = '"+str(1)+"' where syncinvoice_id = '"+str(syncinvoice_id)+"'"
            # print(sql_update_query)
            # print(syncinvoice_id)
            mycursor.execute(sql_update_query)
            mysql.commit()
        else:
            sql_update_query = "UPDATE syncinvoice set flags = '"+str(0)+"' where syncinvoice_id = '"+str(syncinvoice_id)+"'"
            mycursor.execute(sql_update_query)
            mysql.commit()
    except:
        continue
mycursor.close()
mysql.close()
        # if updsql==0:
    #         sql = "INSERT INTO financial_analysis(CompanyNumber, NAME,creditrating, creditscore,creditlimit,revenue) VALUES(%s,%s,%s,%s,%s,%s)"#,combinedcreditscore,combinedpurchasescore)
    #         mycursor.execute(sql,records)
    #         mysql.commit()
    #         mycursor.close()
    #     else:
    #         sql="UPDATE financial_analysis SET creditrating=%s,creditscore=%s,creditlimit=%s,revenue=%s  WHERE CompanyNumber='" + reg + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
    #         mycursor.execute(sql,recds)
    #         mycursor.close()
    #     print(records)
    #     return records
    # except Exception as e:
    #     print(e)
    #     res="Executed with some errors"
    #     return res