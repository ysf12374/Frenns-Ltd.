# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:33:30 2019

@author: Yousuf
"""
def nmzz(namez,frenns,cnb,arg3):
    import mysql.connector
    import numpy as np
    import pandas as pd
    import config
	
    
###########################################################################################################
####### These are mysql queries to select the columns from clearsight_development table  ##################
###########################################################################################################

    mysql = mysql.connector.connect(
      host=config.HOST,
      user=config.USER,
      passwd=config.PSWD,
      database = config.FRENNS_NAME
      )
    df=pd.read_sql('select syncsupplier_id,frenns_id,paid,type,creation_date, collection_date, last_updated,due_date, amount, vat_amount, outstanding_amount,company_number from syncinvoice where name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)
    ff=pd.read_sql('select company_name from syncfinancialanalysis where company_name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)# 

    if namez=='frenns id':
        df=pd.read_sql('select * from syncinvoice where frenns_id = "' + frenns + '" and type="ACCPAY" ', con=mysql)
        ff=pd.read_sql('select company_name from syncfinancialanalysis where company_name = "' + cnb + '" and frenns_id = "' + frenns + '"', con=mysql)# 
    updatesql=ff['company_name']
    updsql=updatesql.as_matrix()
###########################################################################################################
############# Extracting and Converting the values into datetime format  ##################
###########################################################################################################

    creation=df['creation_date']
    collection=df['collection_date']
    update=df['last_updated']
    #dued=df['due_date'] 
    
    creation_time=pd.to_datetime(creation,infer_datetime_format=True)
    collection_time=pd.to_datetime(collection,infer_datetime_format=True)
    last_updated=pd.to_datetime(update,infer_datetime_format=True)
    #dueda=pd.to_datetime(dued,infer_datetime_format=True)
    df['collect_time']=collection_time.dt.date
    df['create_time']=creation_time.dt.date
    df['lastup']=last_updated.dt.date
    #df['DUEDATE']=dueda.dt.date
    df['too']=pd.to_datetime('now')
    f=df['too']
    df['maa']=f.dt.date
    t_t=df['maa']
    cr_t=df['create_time']
    col_t=df['collect_time']
    las_t=df['lastup']
    #due_d=df['DUEDATE']
    from datetime import date, timedelta
    df['total_time']=t_t-cr_t
    df['duedate']=t_t-col_t
    df['last_Updated']=t_t-las_t
    #df['DUE_DATE']=t_t-due_d 
    try:
        lastupdd=df['last_Updated']
        last_upd=lastupdd.astype('timedelta64[D]')
    #last_upd=min(df['last_Updated'])
        try:
            last_updateds=last_upd.astype(int)
        except:
            last_updateds=last_upd#.astype(int)
    except:
        last_updateds=0
    duedat=df['duedate']
    duedays=duedat.astype('timedelta64[D]')
    try:
        DueDate=duedays.astype(int)
    except:
        DueDate=duedays#.astype(int)
    duedatemax=DueDate.sum()/len(DueDate)
    duemax=int(duedatemax)
    year_N=df['collect_time']
    year_num=year_N.astype(str)
    year_number=max(year_num)
    paids=df['paid']
    pai=paids.astype(str)
    paidds=pai.values

    paiD=0;
    for j in range(0,len(paidds)):
        if paidds[j]=='true':
            paiD+=1;
        else:
            pas=0;
    
    create=df['total_time']
    totaltimeinsyastem=create.astype('timedelta64[D]')
    try:
        totalcreationtime=totaltimeinsyastem.astype(int)
    except:
        totalcreationtime=totaltimeinsyastem
    df1=pd.read_sql('select syncsupplier_id,type from syncsupplier where company_name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)
    if namez=='frenns id':
        df1=pd.read_sql('select syncsupplier_id,type from syncsupplier where type = "Supplier" and frenns_id = "' + frenns + '"', con=mysql)

    idd=df['syncsupplier_id']
    syncid=idd.astype(str)
    syncids=syncid.values
    try:
        sync_id=syncids[1]
    except:
        sync_id=0
    
    typee=df['type']
    acc_ty=typee.astype(str)
    account_type=acc_ty.values
    acc_type=min(account_type)

#    try:
#        acc_type=max(account_type)
#    except:
#        acc_type='ACCREC'
    if acc_type=='ACCREC':
        company_type='customer'
    if acc_type=='ACCPAY':
        company_type='supplier'
    
    
    comtypee=df1['type']
    com_ty=comtypee.astype(str)
    compan_type=com_ty.values
    #try:
        #company_type=compan_type[1]
    #except:
        #company_type='Customer'
    
    
    #frennid=df['frenns_id']
    #frnid=frennid.astype(str)
    #frrn=frnid.values
    #frennsid=min(frrn)
    frennsid=frenns
    
    comp_num=df['company_number']
    try:
        company_number=max(comp_num)
    except:
        company_number=''
    if namez=='frenns id':
        df2=pd.read_sql('select * from syncinvoice where frenns_id = "' + frenns + '" ', con=mysql)
        amountz=df2['amount']
        vatamount=df2['vat_amount']
        outstanding=df2['outstanding_amount']
    else:
        amountz=df['amount']
        vatamount=df['vat_amount']
        outstanding=df['outstanding_amount']
    amounts=amountz.astype(float)
    amx=amounts.values
    vatamount=vatamount.astype(float)
    vax=vatamount.values
    outstan=outstanding.astype(float)
    out_standingbal=outstan.values
    z=len(amx)-1
    credit6=0
    credit7=0
###########################################################################################################
        ####### Calculating the Growthrate and ProfitRate  ##################
###########################################################################################################

    revenue=amx+vax
    v=-1
    revlen=len(revenue)
    rev_diff=[]
    growth=0
    growthrate=0
    try:
        while v < len(revenue):
            v+=1
            difference=int(revenue[v]-revenue[v-1])
            if difference<=0:
                growth=0;
            elif difference>0:
                rev_diff.append(difference)
            else:
                ''''''
    except:
        ''''''
    try:
        growth=len(rev_diff)
        times_growth=revlen-growth
        growthrate=100-(((revlen-growth)/float(revlen))*100.00)
    except:
            ''''''
    v=0
    profit=revenue-out_standingbal
    n=-1
    proflen=len(profit)
    progrow=[]
    profitgrowth=0
    profitrate=0
    try:
        while v < len(profit):
            v+=1
            difference=int(profit[v]-profit[v-1])
            if difference<=0:
                profitgrowth=0;
            elif difference>0:
                progrow.append(difference)
            else:
                ''''''
    except:
        ''''''
    try:
        profitgrowth=len(progrow)
        times_profit=proflen-profitgrowth
        profitrate=100-(((proflen-profitgrowth)/float(proflen))*100.00)
    except:
            ''''''   
    
    #j=float(z+1)
    Rev=pd.read_sql('select amount,vat_amount,outstanding_amount from syncinvoice where name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)
    if namez=='frenns id':
        Rev=pd.read_sql('select amount,vat_amount,outstanding_amount from syncinvoice where frenns_id = "' + frenns + '"', con=mysql)
    R_Amount=Rev['amount'].sum()
    R_vat=Rev['vat_amount'].sum()
    R_Outstanding=Rev['outstanding_amount'].sum()
    Revenue=R_Amount+R_vat-R_Outstanding
    
###########################################################################################################
        ####### Calculating the number of times the company is past its due date  ##################
###########################################################################################################

    totalcreation=float(max(totalcreationtime))
    
    if 0<growthrate<=15:
        credit9=86+86;
        purchase7=86-10;
    elif 15<growthrate<=25:
        credit9=81+80;
        purchase7=81-10;
    elif 25<growthrate<=35:
        credit9=76+73;
        purchase7=76-10;
    elif 35<growthrate<=45:
        credit9=70+66;
        purchase7=70-10;
    elif 45<growthrate<=60:
        credit9=63+60;
        purchase7=63-10;
    elif 60<growthrate<=75:
        credit9=59+56;
        purchase7=59-10;
    elif 75<growthrate<=85:
        credit9=57+51;
        purchase7=57-10;
    elif 85<growthrate<=95:
        credit9=51+46;
        purchase7=51-10;
    elif growthrate==0:
        credit9=5;
        purchase7=5;
    else:
        credit9=45+37;
        purchase7=45-10;

    if 0<profitrate<=15:
        credit11=86+84;
        purchase8=86-10;
    elif 15<profitrate<=25:
        credit11=81+78;
        purchase8=81-10;
    elif 25<profitrate<=35:
        credit11=76+71;
        purchase8=76-10;
    elif 35<profitrate<=45:
        credit11=70+67;
        purchase8=70-10;
    elif 45<profitrate<=60:
        credit11=63+61;
        purchase8=63-10;
    elif 60<profitrate<=75:
        credit11=59+51;
        purchase8=59-10;
    elif 75<profitrate<=85:
        credit11=57+50;
        purchase8=57-10;
    elif 85<profitrate<=95:
        credit11=51+46;
        purchase8=51-10;
    elif profitrate==0:
        credit11=5;
        purchase8=5;
    else:
        credit11=45+40; 
        purchase8=45-10;

    paid_range=int(len(paidds)/9)
    if 0<=paiD<=paid_range:
        credit5=51;
    elif paid_range<paiD<=paid_range*2:
        credit5=57;
    elif paid_range*2<paiD<=paid_range*3:
        credit5=61;
    elif paid_range*3<paiD<=paid_range*4:
        credit5=66;
    elif paid_range*4<paiD<=paid_range*5:
        credit5=70;
    elif paid_range*5<paiD<=paid_range*6:
        credit5=76;
    elif paid_range*6<paiD<=paid_range*7:
        credit5=83;
    elif paid_range*7<paiD<=paid_range*9:
        credit5=92;
    else:
        credit5=100;
        
    
###################################################################################################################################
####### Calculating the attributes--> Debt Ratio,TotalTime in the system,Creditlimit,Maximum Days PAst Due Date  ##################
###################################################################################################################################

    sum_amount=amx.sum()
    sum_vat=vax.sum()
    sum_outstanding=out_standingbal.sum()

    sum_a=float(sum_amount)
    sum_va=float(sum_vat)
    sum_out=float(sum_outstanding)

    debtratio=(sum_out/(sum_a+sum_va+1))*100
    if 0<debtratio<=10:
        credit2=99*2;
        purchase0=85;
    elif 10<debtratio<=20:
        credit2=91*2;
        purchase0=80;
    elif 20<debtratio<=30:
        credit2=85*2;
        purchase0=75;
    elif 30<debtratio<=40:
        credit2=76*2;
        purchase0=70;
    elif 40<debtratio<=50:
        credit2=69*2;
        purchase0=60;
    elif 50<debtratio<=70:
        credit2=61*2;
        purchase0=55;
    elif 70<debtratio<=90:
        credit2=58*2;
        purchase0=52;
    elif debtratio==0:
        credit2=95;
        purchase0=95;
    else:
        credit2=51*2;
        purchase0=46;
    if sum_amount==0:
        credit2=15;
        purchase0=15;
    else:
        ''''''
    yea=365
    tcreationtime=totalcreation/float(yea)

    if 0<=tcreationtime<=0.2:
        credit3=48;
        creditlimit=0.05*(sum_a);
    elif 0.2<tcreationtime<=0.4:
        credit3=57;
        creditlimit=0.055*(sum_a);
    elif 0.4<tcreationtime<=0.7:
        credit3=64;
        creditlimit=0.057*(sum_a);
    elif 0.7<tcreationtime<=1:
        credit3=71;
        creditlimit=0.059*(sum_a);
    elif 1<tcreationtime<=2:
        credit3=79;
        creditlimit=0.063*(sum_a);
    elif 2<tcreationtime<=5:
        credit3=86;
        creditlimit=0.12*(sum_a);
    elif 5<tcreationtime<=7:
        credit3=95;
        creditlimit=0.13*(sum_a);
    else: 
        credit3=103;
        creditlimit=0.15*(sum_a);
    
    Creditlimit=int(creditlimit) 
    
    if 0<=duemax<=15:
        credit4=86;
    elif 15<duemax<=30:
        credit4=81;
    elif 30<duemax<=45:
        credit4=74;
    elif 45<duemax<=60:
        credit4=68;
    elif 60<duemax<=90:
        credit4=62;
    else:
        credit4=43;

    Credit_Score=credit2+credit3+credit4+credit5+credit9+credit11;
###########################################################################################################
### Calculating Purchase Score based on Recency , Frequency and the monetary value of the company  ########
###########################################################################################################
    try:
        recency=min(last_updateds) 
    except:
        recency=0
    if 0<=recency<=5:
       purchase1=62;
    elif 5<recency<=10:
        purchase1=85;
    elif 10<recency<=15:
        purchase1=95;
    elif 15<recency<=20:
        purchase1=91;
    elif 20<recency<=50:
        purchase1=84;
    elif 50<recency<=80:
        purchase1=76;
    elif 80<recency<=120:
        purchase1=70;
    elif 120<recency<=150:
        purchase1=60;
    else:
        purchase1=50;

    if 0<=sum_a<50000:
        purchase2=40;
    elif 50000<sum_a<=100000:
        purchase2=60;
    elif 100000<sum_a<=400000:
        purchase2=63;
    elif 400000<sum_a<=750000:
        purchase2=66;
    elif 750000<sum_a<=10000000:
        purchase2=70;
    elif 10000000<sum_a<=50000000:
        purchase2=80;
    elif 50000000<sum_a<=100000000:
        purchase2=90;
    elif 100000000<sum_a<=150000000:
        purchase2=98;
    elif 150000000<sum_a<=250000000:
        purchase2=105;
    elif 250000000<sum_a<=500000000:
        purchase2=109;
    elif sum_a<0:
        purchase2=44;
    else:
        purchase2=113;
    #frequency=z+1
    paids_rang=int(len(paidds)/11)

    if 0<paiD<=paids_rang:
        purchase3=47;
    elif paids_rang<paiD<=paids_rang*2:
        purchase3=50;
    elif paids_rang*2<paiD<=paids_rang*3:
        purchase3=53;
    elif paids_rang*3<paiD<=paids_rang*4:
        purchase3=55;
    elif paids_rang*4<paiD<=paids_rang*5:
        purchase3=57;
    elif paids_rang*5<paiD<=paids_rang*6:
        purchase3=65;
    elif paids_rang*6<paiD<=paids_rang*7:
        purchase3=70;
    elif paids_rang*7<paiD<=paids_rang*8:
        purchase3=75;
    elif paids_rang*8<paiD<=paids_rang*9:
        purchase3=85;
    elif paiD==0:
        purchase3=41;
    elif paids_rang*9<paiD<=paids_rang*11:
        purchase3=89;
    else:
        purchase3=99;
    
    ps=purchase1+purchase2+purchase3+purchase0+purchase7+purchase8;
    Purchase_Score=int(ps)
##########################################################################################
####### Assigning Rating to CreditScores and PurchaseScore from A to H  ##################
##########################################################################################
    if 1<Credit_Score<=470:
        CreditRating='H';
    elif 471<=Credit_Score<=519:
        CreditRating='G';
    elif 520<=Credit_Score<=568:
        CreditRating='F';
    elif 569<=Credit_Score<=617:
        CreditRating='E';
    elif 618<=Credit_Score<=666:
        CreditRating='D';
    elif 667<=Credit_Score<=715:
        CreditRating='C';
    elif 716<=Credit_Score<=764:
        CreditRating='B';
    elif 765<=Credit_Score<=813:
        CreditRating='A';
    else:
        CreditRating='D'
    if 1<Purchase_Score<=300:
        PurchaseRating='H';
    elif 301<=Purchase_Score<=335:
        PurchaseRating='G';
    elif 336<=Purchase_Score<=371:
        PurchaseRating='F';
    elif 372<=Purchase_Score<=406:
        PurchaseRating='E';
    elif 407<=Purchase_Score<=441:
        PurchaseRating='D';
    elif 442<=Purchase_Score<=477:
        PurchaseRating='C';
    elif 478<=Purchase_Score<=512:
        PurchaseRating='B';
    elif 513<=Purchase_Score<=548:
        PurchaseRating='A';
    else:
        PurchaseRating='D'  
    
    if Creditlimit==0:
        Purchase_Score=0;
        Credit_Score=0;
        Creditlimit='ND'
    else:
        ''''''
##############################################################################################
####### Mysql queries to Update or insert into syncfinancialanalysis table  ##################
##############################################################################################
    nammz=namez
    company_name=namez
    records=[str(sync_id),str(company_number),acc_type,company_type,str(company_name),year_number,frennsid,str(Credit_Score),Creditlimit,Purchase_Score,str(Revenue),str(CreditRating),str(PurchaseRating)]
    record=[str(sync_id),acc_type,company_type,str(year_number),str(company_number),str(Credit_Score),Creditlimit,Purchase_Score,str(Revenue),str(CreditRating),str(PurchaseRating)]#str(sync_id),acc_type,company_type,frennsid,year_number,    
    mycursor=mysql.cursor()
#    print(updsql)
    if namez=='frenns id':
        company_number=arg3
        records=[str(sync_id),str(company_number),acc_type,company_type,str(cnb),year_number,frennsid,str(Credit_Score),Creditlimit,Purchase_Score,str(Revenue),str(CreditRating),str(PurchaseRating)]
        record=[str(sync_id),acc_type,company_type,str(year_number),str(company_number),str(Credit_Score),Creditlimit,Purchase_Score,str(Revenue),str(CreditRating),str(PurchaseRating)]
        if len(updsql)==0:
            sql = "INSERT INTO syncfinancialanalysis(syncsupplier_id, company_number,acc_type,company_type,company_name,year_number,frenns_id, creditscore,creditlimit,purchasescore,revenue,creditrating,purchaserating) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql,records)
            mysql.commit()
            mycursor.close()
        else:
            sql="""UPDATE syncfinancialanalysis SET syncsupplier_id=%s,acc_type=%s,company_type=%s,year_number=%s,company_number=%s,creditscore=%s,creditlimit=%s,purchasescore=%s,revenue=%s,creditrating=%s,purchaserating=%s WHERE company_name="{0}"  and frenns_id = "{1}" """.format(cnb,frenns)  #,acc_type=%s,company_type=%s,frenns_id=%s,year_number=%s,                                      
            mycursor.execute(sql,record)
            mysql.commit()
            mycursor.close()
    else:
        if len(updsql)==0:
            sql = "INSERT INTO syncfinancialanalysis(syncsupplier_id, company_number,acc_type,company_type,company_name,year_number,frenns_id, creditscore,creditlimit,purchasescore,revenue,creditrating,purchaserating) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql,records)
            mysql.commit()
            mycursor.close()
        else:
            sql="""UPDATE syncfinancialanalysis SET syncsupplier_id=%s,acc_type=%s,company_type=%s,year_number=%s,company_number=%s,creditscore=%s,creditlimit=%s,purchasescore=%s,revenue=%s,creditrating=%s,purchaserating=%s WHERE company_name="{0}"  and frenns_id = "{1}" """.format(nammz,frenns)  #,acc_type=%s,company_type=%s,frenns_id=%s,year_number=%s,                                      
            mycursor.execute(sql,record)
            mysql.commit()
            mycursor.close()
    mysql.close()
    print(records)


###############################################################################
    ####### Mysql Queries to create drop alter table  ##################
###############################################################################

    #mycursor.execute("drop table vkingsol_frennsdevelopment.sync_payment_analysis")
    #mycursor.execute("ALTER TABLE syncpaymentanalysis drop column name")# company_numberY, creditscoreY, creditlimitY, purchasescoreY)")
    #mycursor.execute("CREATE TABLE sync_payment_aanalysis (name VARCHAR(255), creditscore VARCHAR(255), creditlimit VARCHAR(255), purchasescore VARCHAR(255))")
    #mycursor.execute("select * from syncfinancialanalysis where name = "' + namez + ')
    #sql = "INSERT INTO syncfinancialanalysis (creditscore,creditlimit, purchasescore) VALUES (%s,%s,%s) WHERE company_name="' + namez + '""
#nmzz('BP P.L.C')

#nmzz('KPN B.V.','FRN100000570')
def call(frenns,arg3):
    import mysql.connector
    import numpy as np
    import pandas as pd
    from datetime import date, timedelta
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
        cnb=frenns
    mysql2.close()
    mysql = mysql.connector.connect(
          host=config.HOST,
          user=config.USER,
          passwd=config.PSWD,
          database = config.FRENNS_NAME
          )
    dt=pd.read_sql('select distinct frenns_id,name from syncinvoice where frenns_id="' + frenns + '"', con=mysql)
    name1=dt['name']
    name2=name1.drop_duplicates().reset_index(drop=True)
    name3=np.array(name1)
    fr=dt['frenns_id']
    frn_no_dup=fr.drop_duplicates().reset_index(drop=True)
    frn=np.array(fr)
    try:
        for i in range(0,len(name1)):
                nmzz(name3[i],frn[i],cnb,arg3)
        nmzz('frenns id',frenns,cnb,arg3)
    except Exception as e:
        print(e)
    mysql.commit()
    mysql.close()
#call('FRN100000666','07442456')
#df=nmzz('Lew Plumbing','FRN100000655')
###########################################################################################################
####### Extract Names from syncinvoice table and pass it to the function nmzz one by one  #################
###########################################################################################################
#def com_num(cn,frn):
#    try:
#        import mysql.connector
#        import numpy as np
#        import pandas as pd
#        from datetime import date, timedelta
#        mysql = mysql.connector.connect(
#              host="144.76.137.232",
#              user="vkingsol_demo",
#              passwd="gUj3z5?9",
#              database = "vkingsol_frennsdemo"
#              )
#        jf=pd.read_sql('select distinct name,frenns_id from syncinvoice where company_account_number="' + cn + '"', con=mysql)
#        ff=jf['name']
#        fu=np.array(ff)
#        fr1=jf['frenns_id']
#        frn1=np.array(fr1)
#        if ff.empty:
#            jf=pd.read_sql('select distinct company from marketplace_mpbidding_product where customer_id="' + frn + '"', con=mysql)
#            ff=jf['company']            
#            fu=np.array(ff)
#        for i in range(0,len(fu)):
#            try:
#                nmzz(fu[i],frn1[i])
#            except Exception as e:
#                print(e)
#        if ff.empty:
#                jf=pd.read_sql('select distinct company from marketplace_mpbidding_product where customer_id="' + frn + '"', con=mysql)
#                ff=jf['company']
#                res='Manual Upload'
#                return res   
#        else:
#            res="Done"
#            return res
#    except Exception as e:
#        print(e)
#        res="Executed with some errors"
##        if ff.empty:
##                jf=pd.read_sql('select distinct company from marketplace_mpbidding_product where customer_id="' + frn + '"', con=mysql)
##                ff=jf['company']
##                res='Manual Upload'
##                return res    
#        return res   

##################################################################################
####### Uncomment this section to give input from command line  ##################
##################################################################################


#==============================================================================
# import sys
# arg=sys.argv[1]
# #arg=arg.replace("'","")
# print (arg)
# arg1=sys.argv[2]
# print (arg1)
# #arg1=arg1.replace("'","")
# com_num(arg,arg1)    
# #com_num('02591237','FRN100000570') 
# 
# 
# 
#==============================================================================
