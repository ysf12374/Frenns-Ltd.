# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 12:02:47 2019

@author: Yousuf
"""

# 2019-01-30  oleg.s.solovyev@gmail.com  new code
# 2019-03-03  oleg.s.solovyev@gmail.com  converted python function to file callable with command line: python3 BradfordsLaw.py "FRN100000414"
# description: implement Bradfor's law to mark fraudlent companies

# toDo
#  create function: FRNID, cutoff, password
#  create table if not exist
#  loop over months


def call(frenns_id):
    try:
         # arguments 
        import pandas as pd
        import numpy  as np
        import mysql.connector
        import config
        
        
        
        
        # create connector
        mysql = mysql.connector.connect(
 			host=config.HOST,
     		user=config.USER,
      		passwd=config.PSWD,
      		database = config.FRENNS_NAME
        )
        
        BFL = pd.DataFrame({'BF law first digit':  [np.nan , 0.30103, 0.17609, 0.12494, 0.09691, 0.07918, 0.06695, 0.05799, 0.05115, 0.04576],
                            'BF law second digit': [0.11968, 0.11389, 0.10882, 0.10433, 0.10031, 0.09668, 0.09337, 0.09035, 0.08757, 0.08500]}, 
                                             index=[      0,       1,       2,       3,       4,       5,       6,       7,       8,       9])
        
        # import data
        invoices = pd.read_sql('select amount, creation_date from syncinvoice where frenns_id = "' + frenns_id + '"', con=mysql)
        
        # create table with analysis results and remove values for requested frenns_id
        mysqlcursor = mysql.cursor()
        #mysqlcursor.execute("drop table vkingsol_frennsdevelopment.syncfraudanalysis")
        
        mysqlcursor.execute("\
           create table if not exists vkingsol_frennsdevelopment.syncfraudanalysis (\
               frenns_id varchar(255) not null,\
               datetime timestamp default current_timestamp,\
               area varchar(255) not null,\
               period varchar(100) not null,\
               date_from date not null,\
               date_to date not null,\
               value double not null,\
               anomaly varchar(255) not null,\
               decision varchar(255) not null\
            )"
        )
        
        invoices['invoice first digit']  = invoices.amount.apply(lambda x: str(x)[ :1])
        invoices['invoice second digit'] = invoices.amount.apply(lambda x: str(x)[1:2])
        
        invoices['year'] = pd.to_numeric(invoices.creation_date.astype(str).str[:4])
        ff=pd.read_sql('select value from syncfraudanalysis where area = "Benfords law 1st digit" and frenns_id = "' + frenns_id + '"', con=mysql)
        try:
            updatesql=ff['value']
#            print(len(updatesql))
            updsql=updatesql.as_matrix()
        except:
            updatesql=0
        # loop over mnths
        for year in range(pd.to_numeric(min(invoices.creation_date.astype(str).str[:4])), pd.to_numeric(max(invoices.creation_date.astype(str).str[:4]))+1):
            
            freq1 = pd.to_numeric(invoices.loc[invoices.year == year, 'invoice first digit']).value_counts(normalize=True).sort_index()
            freq2 = pd.to_numeric(invoices.loc[invoices.year == year, 'invoice second digit']).value_counts(normalize=True).sort_index()
            
            BFL = BFL.join(freq1).join(freq2)
            
            z1 = np.nanmax(abs(BFL['BF law first digit' ].cumsum() - BFL['invoice first digit' ].cumsum()))*np.sqrt(invoices.loc[invoices.year == year].shape[0])
            z2 = np.nanmax(abs(BFL['BF law second digit'].cumsum() - BFL['invoice second digit'].cumsum()))*np.sqrt(invoices.loc[invoices.year == year].shape[0])
            z1=z1.mean()
            z2=z2.mean()
            #z1=max(z1)
            #z2=max(z2)
            if len(updatesql)==0:
                sql = "insert into syncfraudanalysis (frenns_id, area, period, date_from, date_to, value, anomaly, decision) values (%s, %s, %s, %s, %s, %s, %s, %s)"
                mysqlcursor.execute(sql, (frenns_id, 'Benfords law 1st digit', 'year', str(year) + '-01-01', str(year) + '-12-31', np.float(z1), '>15', 'yes' if z1>15 else 'no'))
                mysqlcursor.execute(sql, (frenns_id, 'Benfords law 2nd digit', 'year', str(year) + '-01-01', str(year) + '-12-31', np.float(z2), '>15', 'yes' if z2>15 else 'no'))
            
            mysql.commit()
            
            BFL = BFL.drop(['invoice first digit', 'invoice second digit'], axis=1)
            zzz=[frenns_id,z1,z2]
            print(zzz)
        mysqlcursor.close()
        mysql.close()
        return zzz
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
#zzz=call('FRN100000666')
#==============================================================================
# import sys
# frenns_id = sys.argv[1]
#==============================================================================








