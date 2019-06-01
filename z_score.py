# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:31:27 2019

@author: Yousuf
"""
def zscore(frennsid):
    try:
        import mysql.connector
        import numpy as np
        import pandas as pd
        #import matplotlib.pyplot as plt
        import config
        
        mysql = mysql.connector.connect(
      		host=config.HOST,
      		user=config.USER,
      		passwd=config.PSWD,
      		database = config.FRENNS_NAME
          )
        
    # import data
        invoices = pd.read_sql('select amount,outstanding_amount,creation_date,type,vat_amount from syncinvoice where frenns_id ="' + frennsid + '"', con=mysql)
        pp=pd.read_sql('select frenns_id from syncfraudanalysis where frenns_id ="' + frennsid + '" and area="Z Score"', con=mysql)
        try:
            updatesql=pp['frenns_id']
            updsql=len(updatesql)
        except:
            updsql=0;
        
#        try:
#            sqlupdate=pp['id']
#            sqlupd=len(sqlupdate)
#        except:
#            sqlupd=0;
        #url = "E:/per_PPH/new_sync_invoice1 - Copy.csv"
        
        # in case no MySQL connection
        #invoices = pd.read_csv(url)#sep = ';', quotechar = '"'
                               
        creation=invoices['creation_date']
        
        # get year
        #invoices['year'] = invoices.creation_date.apply(lambda x: int(str(x)[ :4]))
        creation_time=pd.to_datetime(creation,infer_datetime_format=True,utc=True)
        invoices['creation_year']=creation_time.dt.year
    
    # sum invoices amount by type and year
        agg = invoices.groupby(['creation_year','type'], as_index=False)['amount'].sum()
        agg1=invoices.groupby(['creation_year','type'], as_index=False)['outstanding_amount'].sum()
        agg2 = invoices.groupby(['creation_year','type'], as_index=False)['vat_amount'].sum()
        
        ### z-score
        agg['z-score'] = (agg.amount - agg.amount.mean())/agg.amount.std(ddof=0)
        agg1['z-score1']= (agg1.outstanding_amount - agg1.outstanding_amount.mean())/agg1.outstanding_amount.std(ddof=0)
        agg2['z-score2'] = (agg2.vat_amount - agg2.vat_amount.mean())/agg2.vat_amount.std(ddof=0)
        
    # get the number of years z-scores have different signs
    ############################################################################
    ### Grouping based on type  and merging all the different score   ##########
    ############################################################################
        d1 = agg.loc[agg['type'] == 'ACCPAY']
        d2 = agg.loc[agg['type'] == 'ACCREC']
        d = d1.merge(d2, on = 'creation_year')
        
        f1 = agg1.loc[agg1['type'] == 'ACCPAY']
        f2 = agg1.loc[agg1['type'] == 'ACCREC']
        f = f1.merge(f2, on = 'creation_year')
        
        k1 = agg2.loc[agg2['type'] == 'ACCPAY']
        k2 = agg2.loc[agg2['type'] == 'ACCREC']
        k = k1.merge(k2, on = 'creation_year')
        
        #s=d.merge(f, on= 'creation_year')
        #final=s.merge(k,on='creation_year')
        # number of times z-scores have different signs
        #f_sum=sum(final['z-score_x']*final['z-score_y'] < 0)+sum(final['z-score1_x']*final['z-score1_y'] < 0)+sum(final['z-score2_x']*final['z-score2_y'] < 0)
        
    #################################################################################    
    #####   Counting the number of times the zscores have different signs #######   
    #################################################################################    
        sum_of_amount=0
        sum_zscore=0
        sum_zscore1=0
        sum_zscore2=0
        for i in range(0,len(agg)+1):
            try:
                if d['z-score_x'][i]<0 and d['z-score_x'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore+=1
                elif d['z-score_x'][i]>0 and d['z-score_x'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore+=1
                elif d['z-score_y'][i]<0 and d['z-score_y'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore+=1
                elif d['z-score_y'][i]>0 and d['z-score_y'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore+=1
                else:
                    sum_of_amount+=0
                    sum_zscore+=0
            except:
                ''''''
        for i in range(0,len(agg)+1):
            try:
                if f['z-score1_x'][i]<0 and f['z-score1_x'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore1+=1
                elif f['z-score1_x'][i]>0 and f['z-score1_x'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore1+=1
                elif f['z-score1_y'][i]<0 and f['z-score1_y'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore1+=1
                elif f['z-score1_y'][i]>0 and f['z-score1_y'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore1+=1
                else:
                    sum_of_amount+=0
                    sum_zscore1+=0
            except:
                ''''''
    
        for i in range(0,len(agg)+1):
            try:
                if k['z-score2_x'][i]<0 and k['z-score2_x'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore2+=1
                elif k['z-score2_x'][i]>0 and k['z-score2_x'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore2+=1
                elif k['z-score2_y'][i]<0 and k['z-score2_y'][i+1]>0:
                    sum_of_amount+=1
                    sum_zscore2+=1
                elif k['z-score2_y'][i]>0 and k['z-score2_y'][i+1]<0:
                    sum_of_amount+=1
                    sum_zscore2+=1
                else:
                    sum_of_amount+=0
                    sum_zscore2+=0
            except:
                ''''''       
        
        
        year=d['creation_year'].values      
        zscore_x=d['z-score_x'].values
        zscore_y=d['z-score_y'].values          
        zscore1_x=f['z-score1_x'].values
        zscore1_y=f['z-score1_y'].values         
        zscore2_x=k['z-score2_x'].values
        zscore2_y=k['z-score2_y'].values
                   
    ################################################################################################
    # Inserting and Updating the z_score table in the database with the calculated zscore values ###               
    ################################################################################################               
        '''for i in range(0,len(year)+1): 
              try:  
                records=[str(frennsid),str(zscore_x[i]),str(year[i]),str(zscore_y[i]),str(zscore1_x[i]),str(zscore1_y[i]),str(zscore2_x[i]),str(zscore2_y[i])]#
                rec=[str(zscore_x[i]),str(year[i]),str(zscore_y[i]),str(zscore1_x[i]),str(zscore1_y[i]),str(zscore2_x[i]),str(zscore2_y[i])]
                if updsql==0:
                    sql="INSERT INTO z_score (frenns_id, zscore_x, year,zscore_y,zscore1_x,zscore1_y,zscore2_x,zscore2_y) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" #         
                    cursor=mysql.cursor()
                    cursor.execute(sql,records)
                    mysql.commit()
                    cursor.close()
                    print(i+1,"Record Inserted into table")
                else:
                    sql="UPDATE z_score SET zscore_x=%s,year=%s,zscore_y=%s,zscore1_x=%s,zscore1_y=%s,zscore2_x=%s,zscore2_y=%s  WHERE frenns_id='" + frennsid + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
                    cursor=mysql.cursor()
                    cursor.execute(sql,rec)
                    cursor.close()
                    print(i+1,"Record Already Exists in the table")
                    
              except:
                 print("End of records ")'''
        
    ################################################################################              
    # Function to calculate the percent deviation of the different sign values #####
    # Note: the fluctuation values can be negative because of the negative zscore###   
    ################################################################################    
        def fluctuate(score):
            try:
               if min(score)<0 and max(score)<0:
                   fluctuation=float(abs(max(score))/abs(min(score)))*100.00
               else:
                   fluctuation=float(min(score)/max(score))*100.00
            except:
                fluctuation=0;
                
            return fluctuation
        
        fluct_x=fluctuate(zscore_x)
        fluct_y=fluctuate(zscore_y)
        fluct1_x=fluctuate(zscore1_x)
        fluct1_y=fluctuate(zscore1_y)
        fluct2_x=fluctuate(zscore2_x)
        fluct2_y=fluctuate(zscore2_y)
        fluctuations=(abs(fluct_x)+abs(fluct_y)+abs(fluct1_x)+abs(fluct1_y)+abs(fluct2_x)+abs(fluct2_y))/6.00
        k=len(zscore_x)
        
        
        if sum_of_amount<=2 and k>0:
            result='No Anomaly Detected'
        elif sum_of_amount>2 and k>0:
            result='Anomaly Detected'
        elif k==0:
            result='Not Enough Data'
        else:
            result='Not Enough Data'
        area='Z Score'
        period='year'
        datefrom=pd.to_numeric(min(invoices.creation_date.astype(str).str[:4]))
        dateto=pd.to_numeric(min(invoices.creation_date.astype(str).str[:4]))
        datefrom=str(dateto)+"-01-01"
        dateto=str(dateto)+"-12-31"
        anomaly='<=2'
        records=[str(frennsid),area,period,str(datefrom),str(dateto),str(sum_of_amount),anomaly,result]
        recds=[str(sum_of_amount),result]

        
    #############################################################################################   
    # We generate an analysis report in a new table named z_score_analysis and insert or update #
    # the number of times the z score's have different times and its fluctuation and also the   #
    # analysis of the values calculated above into the result column                            #
    #############################################################################################  
        '''try:
            record=[str(frennsid),str(sum_of_amount),str(sum_zscore),str(sum_zscore1),str(sum_zscore2),str(fluctuations),str(result)]
            recds=[str(sum_of_amount),str(sum_zscore),str(sum_zscore1),str(sum_zscore2),str(fluctuations),str(result)]
            if sqlupd==0:
                    sql="INSERT INTO z_score_analysis (frenns_id, total_deviation_count,zscore_deviation_count,zscore1_deviation_count,zscore2_deviation_count, fluctuation, result ) VALUES (%s,%s,%s,%s,%s,%s,%s)" #         
                    cursor=mysql.cursor()
                    cursor.execute(sql,record)
                    mysql.commit()
                    cursor.close()
                    print("Record Inserted into table",records)
            else:
                    sql="UPDATE z_score_analysis SET total_deviation_count=%s,zscore_deviation_count=%s,zscore1_deviation_count=%s,zscore2_deviation_count=%s,fluctuation=%s, result=%s  WHERE frenns_id='" + frennsid + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
                    cursor=mysql.cursor()
                    cursor.execute(sql,recds)
                    cursor.close()
                    print("Record Already Exists in the table",recds)
                    
        except:
            print("End of records")'''
        
        

        if updsql==0:
                sql="INSERT INTO syncfraudanalysis (frenns_id,area,period,date_from,date_to,value,anomaly,decision) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" #         
                cursor=mysql.cursor()
                cursor.execute(sql,records)
                mysql.commit()
                cursor.close()
                print("Record Inserted into table",records)
            
        else:
                sql="UPDATE syncfraudanalysis SET value=%s,decision=%s  WHERE frenns_id='" + frennsid + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
                cursor=mysql.cursor()
                cursor.execute(sql,recds)
                cursor.close()
                print("Record Already Exists in the table",recds)
        mysql.close()            
        return records
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
        #print("End of records")
    
    #print (sum_of_amount,sum_zscore,sum_zscore1,sum_zscore2,frennsid)           

####################################################################################################
##Connecting to the server and collecting Frennsid of all the companies                          ###
############Note- Change the host value to localhost when running on a local server#################
####################################################################################################
#zscore('FRN100000632')
#==============================================================================
# import mysql.connector
# import numpy as np
# import pandas as pd
# #import matplotlib.pyplot as plt   
# mysql = mysql.connector.connect(
#       host="144.76.137.232",
#       user="vkingsolextadmin",
#       passwd="~O3o3y4h",
#       database = "vkingsol_frennsdevelopment"
#       )
# data=pd.read_sql('select frenns_id from syncinvoice', con=mysql)
# frenns=data['frenns_id']
# frenns_without_duplicates=frenns.drop_duplicates().reset_index(drop=True)
# frenns_array=np.array(frenns_without_duplicates)
# for i in range(0,len(frenns_array)):
#         zscore(frenns_array[i])
# mysql.commit()
# mysql.close()
# 
#==============================================================================
#zscore('FRN100000414')

#==============================================================================
#==============================================================================
# # import sys
# # arg=sys.argv[1]
# # zscore(arg)
#==============================================================================
#==============================================================================

          