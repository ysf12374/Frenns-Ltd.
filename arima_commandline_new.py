# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:51:51 2019

@author: Yousuf
"""
#import csv, sys, os, pytz, datetime, json, re
##import settings, database
##from pyramid.arima import auto_arima
#from random import random
#from pandas import read_csv
#from pandas import datetime
#from pandas import DataFrame
#import mysql.connector
#import numpy as np
#import pandas as pd
#from statsmodels.tsa.arima_model import ARIMA 
##import matplotlib.pyplot as plt   
#
#mysql = mysql.connector.connect(
#      host="localhost",
#      user="vkingsol_frennsdemo",
#      passwd="gUj3z5?9h",
#      database = "vkingsol_frennsdemo"
#      )
#
import warnings
from pandas import Series
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
# 
## evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
        import warnings
        from pandas import Series
        from statsmodels.tsa.arima_model import ARIMA
        from sklearn.metrics import mean_squared_error
    	# prepare training dataset
        train_size = int(len(X) * 0.66)
        train, test = X[0:train_size], X[train_size:]
        history = [x for x in train]
    	# make predictions
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=arima_order)
            model_fit = model.fit(disp=0)
            yhat = model_fit.forecast()[0]
            predictions.append(yhat)
            history.append(test[t])
    	# calculate out of sample error
        error = mean_squared_error(test, predictions)
        print(error)
        return error

# 
## evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
    	for d in d_values:
    		for q in q_values:
    			order = (p,d,q)    
    			try:
    				mse = evaluate_arima_model(dataset, order)
    				if mse < best_score:
    					best_score, best_cfg = mse, order
    				print('ARIMA%s MSE=%.3f' % (order,mse))
    			except:
    				continue
    print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
    return best_cfg
#
## load dataset
#frn_id   = 'FRN100000414'
#i='BP P.L.C'
#df=pd.read_sql("select DISTINCT name from syncinvoice where frenns_id = '{0}'".format(frn_id), con=mysql)
#name=df['name'].values.astype(str)
#
#qr=pd.read_sql("SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(collection_date) as pay_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' and name='{1}' order by issue_date desc ".format(frn_id,i),con=mysql)
#ser=qr[['issue_date','after_issue_days']]
#ser.to_csv("series.csv")
#series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
## evaluate parameters

#warnings.filterwarnings("ignore")
#orderr=evaluate_models(series.values, p_values, d_values, q_values)
#stepwise_model = ARIMA(series, order=orderr)
##train = series.loc[st,p,d,qr(init_dt):str(last_dt)]
#model_fit=stepwise_model.fit(disp=0)
#output=model_fit.forecast()
#out1=max(output[0])

def ysf(frn_id):
    import csv, sys, os, pytz, datetime, json, re
    import warnings
    #import settings, database
    #from pyramid.arima import auto_arima
    from random import random
    from pandas import read_csv
    from pandas import datetime
    from pandas import DataFrame
    import mysql.connector
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.arima_model import ARIMA 
    import config
    #import matplotlib.pyplot as plt   
    
    mysql = mysql.connector.connect(
      host=config.HOST,
      user=config.USER,
      passwd=config.PSWD,
      database = config.FRENNS_NAME

          )

    
    #ff=pd.read_sql('select company_name,expected_days,average_payment_days from syncfinancialanalysis where company_name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)# 
    #updatesql=ff['expected_days']
    #updsql=updatesql.as_matrix()
    #updd=ff['average_payment_days']
    #updd1=updd.as_matrix()
    #cursor = mysql.cursor()
    #onlyAmt = []
    #frn_id   = 'FRN100000534'
    #year_num = '2019'
    #tp_type  = 'ACCREC'
    #qry_1 = "select DISTINCT name from `syncinvoice` where `frenns_id` = '{0}';".format(frn_id)
    #csr_1 = mysql.cursor()
    #csr_1.execute(qry_1)
    #the_sync_ids = []
    #the_sync_ids_int = []
    #name=[]
    try:

        df=pd.read_sql("select DISTINCT name from syncinvoice where frenns_id = '{0}'".format(frn_id), con=mysql)
        #for rec in csr_1:
        #    name.append(rec)
        #zzz=name[2]
        #zzz=zzz[0]
        #y=np.asarray(name)
        #name=np.asarray(df['name'])
        name=df['name'].values.astype(str)
        #name='qbCompnay'
        p_values = [0, 1, 2, 4, 6, 8, 10]
        d_values = range(0, 3)
        q_values = range(0, 3)
        #compare_date = str(year_num)+'-12-31 23:59:59'
        out=[]
        average=[]
        rec=[]
#        qr=pd.read_sql("""SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(collection_date) as pay_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' order by issue_date desc """.format(frn_id),con=mysql)
#        print qr
#        ser=qr[['issue_date','after_issue_days']]
#        ser.to_csv("series.csv")
#        series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
#        series=series.astype('float32')
#        os.remove("series.csv")
#        orderr=evaluate_models(series.values, p_values, d_values, q_values)
        for i in name:

            import warnings
            qr=pd.read_sql("""SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(collection_date) as pay_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' and name = "{1}" order by issue_date desc """.format(frn_id,i),con=mysql)
            ser=qr[['issue_date','after_issue_days']]
            if len(ser)>1:
                ser.to_csv("series.csv")
                series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
                from matplotlib import pyplot
                #from pandas.tools.plotting import autocorrelation_plot
                warnings.filterwarnings("ignore")
                avg=int(qr['after_issue_days'].mean())
                average.append(avg)
                #ser.plot()
                #autocorrelation_plot(series)
                #pyplot.show()  
                #X=series.values
                series=series.astype('float32')
                os.remove("series.csv")   
                
                stepwise_model = ARIMA(series, order=(0,0,0))
                #train = series.loc[st,p,d,qr(init_dt):str(last_dt)]
                model_fit=stepwise_model.fit(disp=0)
                output=model_fit.forecast()
                out1=int(max(output[0]))
                out.append(out1)
                ##############################################################################################
            ####### Mysql queries to Update or insert into syncfinancialanalysis table  ##################
            ##############################################################################################
                
             
                records=[str(frn_id),str(i),str(out1),str(avg)]
                rec.append(records)
                print(records)
            else:
                avg=int(qr['after_issue_days'].mean())
                average.append(avg)
                out1=int(qr['after_issue_days'].mean())
                out.append(out1)
                records=[str(frn_id),str(i),str(out1),str(avg)]
                rec.append(records)
        return rec
    except Exception as e:
        print (e)

def yousuf(frn_id):
    import csv, sys, os, pytz, datetime, json, re
    import warnings
    from random import random
    from pandas import read_csv
    from pandas import datetime
    from pandas import DataFrame
    import mysql.connector
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.arima_model import ARIMA 
    import config
    mysql = mysql.connector.connect(
      host=config.HOST,
      user=config.USER,
      passwd=config.PSWD,
      database = config.FRENNS_NAME)
    try:
        name='frenns id'
        p_values = [0, 1, 2, 4, 6, 8, 10]
        d_values = range(0, 3)
        q_values = range(0, 3)
        out=[]
        average=[]
        rep=[]
        import warnings
        qr=pd.read_sql("""SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(collection_date) as pay_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' and type = "ACCPAY" order by issue_date desc """.format(frn_id),con=mysql)
        ser=qr[['issue_date','after_issue_days']]
        if len(ser)>1:
            ser.to_csv("series.csv")
            series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
            from matplotlib import pyplot
            #from pandas.tools.plotting import autocorrelation_plot
            warnings.filterwarnings("ignore")
            avg=int(qr['after_issue_days'].mean())
            average.append(avg)
            #ser.plot()
            #autocorrelation_plot(series)
            #pyplot.show()  
            #X=series.values
            series=series.astype('float32')
            os.remove("series.csv")   
            
            stepwise_model = ARIMA(series, order=(0,0,0))
            #train = series.loc[st,p,d,qr(init_dt):str(last_dt)]
            model_fit=stepwise_model.fit(disp=0)
            output=model_fit.forecast()
            out1=int(max(output[0]))
            out.append(out1)
            ##############################################################################################
        ####### Mysql queries to Update or insert into syncfinancialanalysis table  ##################
        ##############################################################################################
            
         
            records=[str(frn_id),str(name),str(out1),str(avg)]
            rep.append(records)
            print(records)
        else:
            avg=int(qr['after_issue_days'].mean())
            average.append(avg)
            out1=int(qr['after_issue_days'].mean())
            out.append(out1)
            records=[str(frn_id),str(name),str(out1),str(avg)]
            rep.append(records)
        return rep
    except Exception as e:
        print (e)


#        import mysql.connector
#
#        mysql1 = mysql.connector.connect(
#              host="144.76.137.232",
#              user="clearsightext",
#              passwd="gR985xi*",
#              database = "clearsight_development"
#              )
#        mycursor=mysql1.cursor()
#        sql = "INSERT INTO financial_analysis(CompanyNumber,NAME,expected_days,average_payment_days)  VALUES(%s,%s,%s,%s)"#select expected_days,average_payment_days from syncfinancialanalysis where company_name='" + i + "'  and frenns_id = '" + frn_id + "'
#        #sql="UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s WHERE company_name='" + i + "'  and frenns_id = '" + frn_id + "'"
#        mycursor.execute(sql,records)
#        mysql1.commit()
#        mycursor.close()
#        mysql1.close()
#    
 

import mysql.connector
import numpy as np
import pandas as pd
from datetime import date, timedelta
import csv
import config
#mysql = mysql.connector.connect(
#      host="144.76.137.232",
#      user="vkingsolextadmin",
#      passwd="~O3o3y4h",
#      database = "vkingsol_frennsdevelopment"
#      )
#jf=pd.read_sql('select DISTINCT frenns_id from syncinvoice', con=mysql)
##ff=jf['name']
##kin=ff.drop_duplicates().reset_index(drop=True)
##fu=np.array(ff)
#fr1=jf['frenns_id']
#frn1_no_dup=fr1.drop_duplicates().reset_index(drop=True)
#frn1=np.array(fr1)

def name(arg,arg2):
    import mysql.connector
    import config
    mysql = mysql.connector.connect(
      host=config.HOST,
      user=config.USER,
      passwd=config.PSWD,
      database = config.FRENNS_NAME
          )
    df=pd.read_sql("select DISTINCT name from syncinvoice where frenns_id = '{0}' and company_number='{1}'".format(arg,arg2), con=mysql)
    name=df['name'].values.astype(str)
    return name


def call(arg,arg3):
    from pandas import read_csv
    import mysql.connector
    import numpy as np
    import pandas as pd
    try:
                #nm=name(arg,arg2)
        clr_rec=[]
        clr_rec.extend(ysf(arg))
        clr_rec.extend(yousuf(arg))
        #for i in range(0,len(frn1)):
        #        df=pd.read_sql("SELECT date(issue_date) as issue_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' order by issue_date desc ".format(frn1[i]),con=mysql)
        #        ser=df[['issue_date','after_issue_days']]
        #        ser.to_csv("series.csv")
        #        series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
        #        warnings.filterwarnings("ignore")
        #        orderr=evaluate_models(series.values, p_values, d_values, q_values)
        #        clr_rec.extend(ysf(frn1[i],orderr))
        #        #nmzz(fu[i])
        #    
        #mysql.close()
        import config
    
        mysql2 = mysql.connector.connect(
                      host=config.HOST,
                      user=config.USER,
                      passwd=config.PSWD,
                      database = config.CLEARSIGHT_NAME
                      )
        cnb=pd.read_sql("""select CompanyName from company_data where CompanyNumber="{0}" """.format(arg3),con=mysql2)
        cnb=cnb['CompanyName']
        try:
            cnb=max(cnb)
        except:
            cnb=arg
        mysql2.close()
        for j in range(0,len(clr_rec)):
            mysql1 = mysql.connector.connect(
                  host=config.HOST,
                  user=config.USER,
                  passwd=config.PSWD,
                  database = config.FRENNS_NAME
                  )
            mycursor=mysql1.cursor()
            records=clr_rec[j]
            record=[records[0],records[1],records[2],records[3],records[3],records[3]]
            recd=[records[2],records[3],records[3],records[3]]
            nm=str(records[1])
            update1=[]
            if nm=='frenns id':
                record1=[records[0],cnb,records[2],records[3],records[3],records[3]]
                recd1=[records[2],records[3],records[3],records[3]]
                upd=pd.read_sql("""select company_name from syncfinancialanalysis where company_name = "{0}"  and frenns_id="{1}" """.format(cnb,arg), con=mysql1)
                update=upd['company_name']
                update1=update.as_matrix()
                if len(update1)==0:
                    sql="""INSERT INTO syncfinancialanalysis(frenns_id,company_name,expected_days,average_payment_days,company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
                    mycursor.execute(sql,record1)
                else:
                    sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and frenns_id="{1}" """.format(cnb,arg)
                    mycursor.execute(sql,recd1) 
            else:       
                upd=pd.read_sql("""select company_name from syncfinancialanalysis where company_name = "{0}"  and frenns_id="{1}" """.format(nm,arg), con=mysql1)
                update=upd['company_name']
                update=update.as_matrix()
            #            if len(update)==0:
            #                sql="""INSERT INTO syncfinancialanalysis(frenns_id,company_name,expected_days,average_payment_days) VALUES(%s,%s,%s,%s)"""
            #                mycursor.execute(sql,record)     
            #            else:
            #            sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s WHERE company_name="{0}" """.format(records[1])
            #            mycursor.execute(sql,recd) 
                    
            #            sql = "INSERT INTO financial_analysis(CompanyNumber,NAME,expected_days,average_payment_days)  VALUES(%s,%s,%s,%s)"#select expected_days,average_payment_days from syncfinancialanalysis where company_name='" + i + "'  and frenns_id = '" + frn_id + "'                                                                                                
            
                if len(update)==0:
                    sql="""INSERT INTO syncfinancialanalysis(frenns_id,company_name,expected_days,average_payment_days,company_deliquency_score,company_paydex_score) VALUES(%s,%s,%s,%s,%s,%s)"""
                    mycursor.execute(sql,record)
                else:
                    sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s,company_deliquency_score=%s,company_paydex_score=%s WHERE company_name="{0}" and frenns_id="{1}" """.format(nm,arg)
                    mycursor.execute(sql,recd) 
            mysql1.commit()
            mycursor.close()
            mysql1.close()
    
            print(record)
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
#call('FRN100000666','07442456')
#arg='FRN100000626'
    
#from pandas import read_csv
#import mysql.connector
#import numpy as np
#import pandas as pd
#
#    #nm=name(arg,arg2)
#clr_rec=[]
#clr_rec.extend(ysf(arg))
##for i in range(0,len(frn1)):
##        df=pd.read_sql("SELECT date(issue_date) as issue_date, COALESCE(DATEDIFF(date(collection_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days FROM `syncinvoice` where frenns_id = '{0}' order by issue_date desc ".format(frn1[i]),con=mysql)
##        ser=df[['issue_date','after_issue_days']]
##        ser.to_csv("series.csv")
##        series = read_csv("series.csv", header=0, parse_dates=[0], index_col=1, squeeze=True).drop(['Unnamed: 0'],axis=1)
##        warnings.filterwarnings("ignore")
##        orderr=evaluate_models(series.values, p_values, d_values, q_values)
##        clr_rec.extend(ysf(frn1[i],orderr))
##        #nmzz(fu[i])
##    
##mysql.close()
#
#for j in range(0,len(clr_rec)):
#    import config
#    mysql1 = mysql.connector.connect(
#                  host=config.HOST,
#                  user=config.USER,
#                  passwd=config.PSWD,
#                  database = config.FRENNS_NAME
#                  )
#    mycursor=mysql1.cursor()
#    records=clr_rec[j]
#    record=[records[0],records[1].replace("'","''"),records[2],records[3]]
#    recd=[records[2],records[3]]
#    print(record)
#    nm=str(records[1])
#    #sql = "INSERT INTO financial_analysis(CompanyNumber,NAME,expected_days,average_payment_days)  VALUES(%s,%s,%s,%s)"#select expected_days,average_payment_days from syncfinancialanalysis where company_name='" + i + "'  and frenns_id = '" + frn_id + "'                                                                                                
#    try:
#        sql="""INSERT INTO syncfinancialanalysis(frenns_id,company_name,expected_days,average_payment_days) VALUES(%s,%s,%s,%s)"""
#        mycursor.execute(sql,record)
#    except:
#        sql="""UPDATE syncfinancialanalysis SET expected_days=%s,average_payment_days=%s WHERE NAME={0}""".format(nm)
#        mycursor.execute(sql,recd) 
#    mysql1.commit()
#    mycursor.close()
#    mysql1.close()

#==============================================================================
# import sys
# arg=sys.argv[1]
# #arg='FRN100000570'
# print (arg)
# arg2=sys.argv[2]
# print (arg2)
# #arg2='00542515'
# call(arg,arg2)    
#==============================================================================