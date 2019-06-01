
def regnum(reg):  
    
    try:
        import numpy as np
        import pandas as pd
        import mysql.connector
        import config
        mysql = mysql.connector.connect(
          host=config.HOST,
          user=config.USER,
          passwd=config.PSWD,
          database = config.CLEARSIGHT_NAME
          )
    ###########################################################################################################
    ####### These are mysql queries to select the columns from clearsight_development table  ##################
    ###########################################################################################################
        
        df = pd.read_sql('select * from company_ann_reports where CompanyNumber = "' + reg + '"', con=mysql)
        if df.empty:
            reg=reg
            naame=''
            CreditRating='NB'
            CreditScore='NB'
            creditlimits='NB'
            revv='NB'
            records=[str(reg), str(naame),str(CreditRating),str(CreditScore),creditlimits,str(revv)]
            #resultz="Company Not Found "
            #print (resultz)
            return records
        else:
            llf=pd.read_sql('select CompanyStatus,AccountsNextDueDate,IncorporationDate from company_data where CompanyNumber="' + reg + '"', con=mysql)
            pp=pd.read_sql('select NAME from financial_analysis where CompanyNumber ="' + reg + '"', con=mysql)
            try:
                updatesql=pp['NAME']
                updsql=len(updatesql)
            except:
                updsql=0;
        ####################################################################################################
        #####  Extracting the status value of the company and assigning 1 if active and 0 otherwise  #######
        ####################################################################################################
            stat=llf['CompanyStatus']
            status=stat.as_matrix()
            statust=2;
            try:
                com_stat=status[0]
                if com_stat=='Active' or com_stat=='Active - Proposal to Strike off':
                    statust=1;
                else:
                    statust=0;
            except:
                ''''''
        ####################################################################################################################
        ####### Extracting the values of the attributes from the dataframe and converting to matrix  #######################
        ####### Changet the strings inside the dataframe (df) if the name of the attribute changes in the table    #########
        ####################################################################################################################
            
            try:
                import datetime
                creation=llf['IncorporationDate']
                creation_time=pd.to_datetime(creation,infer_datetime_format=True)
                llf['creation_days']=creation_time.dt.date
                llf['too']=pd.to_datetime('now')
                f=llf['too']
                llf['maa']=f.dt.date
                t_t=llf['maa']
                cr_t=llf['creation_days']
                llf['total_time']=t_t-cr_t
                create=llf['total_time']
                totaltimeinsyastem=create.astype('timedelta64[D]')
                totalcreationtime=totaltimeinsyastem.astype(int)
                incorporate_days=max(totalcreationtime)
            except:
                incorporate_days=100;
            
            
            try:
                creation=llf['AccountsNextDueDate']
                creation_time=pd.to_datetime(creation,infer_datetime_format=True)
                llf['duedate_days']=creation_time.dt.date
                llf['too']=pd.to_datetime('now')
                f=llf['too']
                llf['maa']=f.dt.date
                t_t=llf['maa']
                cr_t=llf['duedate_days']
                llf['duedate']=t_t-cr_t
                duedate=llf['duedate']
                duedays=duedate.astype('timedelta64[D]')
                duedateindays=duedays.astype(int)
                due_date_days=max(duedateindays)
            except:
                due_date_days=90;
            
            yerr=df['YEAR']
            yr=yerr.as_matrix()
            years=max(yr)
        
            namm=df['NAME']#EXTRACTING NAME
            nm=namm.as_matrix()
            naame=max(nm)
            
            ch=df.cash.as_matrix()
            cash=ch.mean()
            
            fxx=df['fix_ass']
            fix=fxx.as_matrix()
            fixass=fix.mean()
            
            
            ta=df['tot_ass']
            tass=ta.as_matrix()
            totas=max(tass)
            totalass=tass.mean()
            
            longterm=df['Long_term_d']
            longdeb=longterm.as_matrix()
            longdebt=longdeb.mean()
                     
            cl=df['curr_lia']
            currli=cl.as_matrix()
            currliab=currli.mean()
            
            pnlbef=df['pnl_before_tax']
            pnlbef=pnlbef.as_matrix()
            pnlbef=pnlbef.mean()
            pnlaft=df['pnl_after_tax']
            pnlaft=pnlaft.as_matrix()
            pnlaft=pnlaft.mean()   
            pnl=abs((pnlbef+pnlaft)/2.0)
            
            grossprofit=df['grossprofit']
            grossprofit=grossprofit.as_matrix()
            grossprofit=abs(grossprofit.mean())
            
            depr=df['depr_amort']
            if max(depr)<0:
                depr_amort=2;
                credit9=11;
            elif max(depr)>0:
                depr_amort=1;
                credit9=26;
            elif max(depr)==0:
                depr_amort=0;
                credit9=0;
            else:
                kl=0;
            
            
            
        
        
        ################################################################################
        ######  EXTRACTING CREDIT AND PURCHASE SCORES FROM FRENNSID TABLE ##############
        #####  Comment this out and use if the script is taking too long   #############
        ##### and move a copy of the syncfinancialanalysis into clearsight database  ###
        ################################################################################
    
        ##################################################################################################################################################
        ####    Assigning a temporary score value to all the attributes which would be added up later to get the final score          ####################
        #### Attributes Include--> Owners Equity, Debt Ratio, Total Assets, Long Debt and Current Liabilities  <--########################################
        ##################################################################################################################################################
            debtr=(currliab/(float(totalass)+1))*100.00
            ownersequity=float(totalass-currliab)
            
            if ownersequity<=-10000000:
                credit0=45;
            elif -10000000<ownersequity<0:
                credit0=47;
            elif ownersequity==0:
                credit0=20;
            elif 0<ownersequity<=10000:
                credit0=50;
            elif int(10000)<ownersequity<=int(100000):
                credit0=53;
            elif 100000<ownersequity<=250000:
                credit0=75;
            elif 250000<ownersequity<=500000:
                credit0=86;
            elif 500000<ownersequity<=1000000:
                credit0=94;
            elif 1000000<ownersequity<=10000000:
                credit0=105;
            else:
                credit0=119;
            
            if 0<debtr<=10:
                credit1=142;
                purchase2=110*2;
            elif debtr==0:
                credit1=35;
                purchase2=22*2;
            elif 10<debtr<=25:
                credit1=135;
                purchase2=104*2;
            elif 25<debtr<=35:
                credit1=128;
                purchase2=92*2;
            elif 35<debtr<=50:
                credit1=119;
                purchase2=85*2;
            elif 50<debtr<=60:
                credit1=110;
                purchase2=78*2;
            elif 60<debtr<=70:
                credit1=101;
                purchase2=75*2;
            elif 70<debtr<=85:
                credit1=90;
                purchase2=70*2;
            elif 85<debtr<=90:
                credit1=78;
                purchase2=64*2;
            elif 90<debtr<=100:
                credit1=66;
                purchase2=60*2;
            elif 100<debtr<=200:
                credit1=52;
                purchase2=54*2;
            elif 200<debtr<=400:
                credit1=53;
                purchase2=50*2;
            elif debtr<=0:
                credit1=150;
                purchase2=119*2;
            else:
                credit1=50;
                purchase2=45*2;
            
        
            if totalass<-3000000:
                credit2=29;
            elif -3000000<totalass<0:
                credit2=32;
            elif totalass==0:
                credit2=20;
            elif 0<totalass<=100000:
                credit2=35;
            elif 100000<totalass<=500000:
                credit2=38;
            elif 500000<totalass<=1000000:
                credit2=42;
            elif 1000000<totalass<=5000000:
                credit2=47;
            elif 5000000<totalass<=10000000:
                credit2=51;
            elif 10000000<totalass<=50000000:
                credit2=56;
            else:
                credit2=60;
            
            if longdebt<0:
                credit3=121;
                purchase3=121;
            elif longdebt==0:
                credit3=25;
                purchase3=34;
            elif 0<longdebt<=5000:
                credit3=108;
                purchase3=108;
            elif 5000<longdebt<=10000:
                credit3=110;
                purchase3=121;
            elif 10000<longdebt<=50000:
                credit3=99;
                purchase3=99;
            elif 50000<longdebt<=100000:
                credit3=87;
                purchase3=86;
            elif 100000<longdebt<=500000:
                credit3=81;
                purchase3=80;
            elif 500000<longdebt<=1000000:
                credit3=78;
                purchase3=77;
            elif 1000000<longdebt<=5000000:
                credit3=71;
                purchase3=70;
            elif 5000000<longdebt<=20000000:
                credit3=66;
                purchase3=65;
            else:
                credit3=61;
                purchase3=60;
        
            if currliab<=0:
                credit4=111;
            elif 0<currliab<=5000:
                credit4=108;
            elif 5000<currliab<=10000:
                credit4=110;
            elif 10000<currliab<=50000:
                credit4=99;
            elif 50000<currliab<=100000:
                credit4=87;
            elif 100000<currliab<=500000:
                credit4=81;
            elif 500000<currliab<=1000000:
                credit4=78;
            elif 1000000<currliab<=5000000:
                credit4=71;
            elif 5000000<currliab<=20000000:
                credit4=66;
            else:
                credit4=61;
        #####################################################################################
        ####    Calculating Creditlimit and adding up the scores gathered from above  #######
        #####################################################################################
            purchase5=0
            yea=365
            incorporate_daz=incorporate_days/float(yea)
            
            cash=df['cash'].mean()
            work=df['work_cap'].mean()
            sales=df['sales'].mean()
            if sales==0 and cash==0 and work==0:
                revv=sales
        
            if cash>0 or sales>0 or work>0:
                revv=abs(cash+sales)
        
            if sales>0:
                revv=sales
                
            if 0<=incorporate_daz<=1:
                credit5=48;
                purchase7=48;
                creditl=(17.00/100.00)*(revv)
            elif incorporate_days==100:
                credit5=12;
                purchase7=12;
                creditl=(16.00/100.00)*(revv)
            elif 1<incorporate_daz<=2:
                credit5=57;
                purchase7=57;
                creditl=(18.00/100.00)*(revv)
            elif 2<incorporate_daz<=3:
                credit5=64;
                purchase7=64;
                creditl=(20.00/100.00)*(revv);
            elif 3<incorporate_daz<=4:
                credit5=71;
                purchase7=71;
                creditl=(24.00/100.00)*(revv);
            elif 4<incorporate_daz<=5:
                credit5=79;
                purchase7=79;
                creditl=(25.00/100.00)*(revv);
            elif 5<incorporate_daz<=6:
                credit5=86;
                purchase7=86;
                creditl=(27.00/100.00)*(revv);
            elif 6<incorporate_daz<=7:
                credit5=95;
                purchase7=95;
                creditl=(30.00/100.00)*(revv);
            elif incorporate_daz>7: 
                credit5=103;
                purchase7=103;
                creditl=(35.00/100.00)*(revv);
            else:
                credit5=25;
                purchase7=25;
                creditl=0;
                
            if 0<due_date_days<=90:
                credit6=86;
                purchase6=76;
            elif due_date_days==90:
                credit6=13;
                purchase6=14;
            elif due_date_days==0:
                credit6=50;
                purchase6=50;
            elif due_date_days<0:
                credit6=97;
                purchase6=91;
            elif 90<due_date_days<=120:
                credit6=71;
                purchase6=67;
            elif 120<due_date_days<=180:
                credit6=62;
                purchase6=58;
            else:
                credit6=43;
                purchase6=35;
            creditlimit=int(creditl)
            
            if creditlimit<0:
                purchase5=-50;
            elif creditlimit==0:
                purchase5=-25;
            else:
                purchase5=0;
            
            if pnl==0:
                credit7=0;
            elif 0<pnl<=5000:
                credit7=25;
            elif 5000<pnl<=5000000:
                credit7=35;
            elif pnl>5000000:
                credit7=43;
            else:
                kl=0;
            
            if grossprofit==0:
                credit8=0;
                purchase8=0;
            elif 0<grossprofit<=1000:
                credit8=32;
                purchase8=32;
            elif 1000<grossprofit<=3000:
                credit8=39;
                purchase8=39;
            elif 3000<grossprofit<=5500:
                credit8=44;
                purchase8=44;
            elif 5500<grossprofit<8000:
                credit8=48;
                purchase8=48;
            elif 8000<grossprofit<=25000:
                credit8=53;
                purchase8=53;
            elif 25000<grossprofit<=50000:
                credit8=59;
                purchase8=59;
            elif 50000<grossprofit<=95000:
                credit8=65;
                purchase8=65;
            elif grossprofit>95000:
                credit8=71;
                purchase8=71;
            else:
                kl=0;
            
            CreditS=credit0+credit1+credit2+credit3+credit4+credit5+credit6+credit7+credit8+credit9
            PurchaseS=purchase2+purchase3+purchase5+purchase6+purchase7+purchase8
            
            PurchaseScore=int(PurchaseS)
            CreditScore=int(CreditS) 
        ##############################################################################
        ####Check the company's Status and Assigning 'ND' if the creditlimit is 0#####
        ##############  And 'LD' if the Company is liquidated  #######################
        ##############################################################################   
            if creditlimit==0:
                credit='ND';
                PurchaseScore=0;
                CreditScore=0;
            else:
                kl=0;
            if creditlimit==0 and statust==0:
                credit='LD';
                PurchaseScore=0;
                CreditScore=0;
            elif creditlimit==0 and statust==1:
                credit='ND';
                PurchaseScore=0;
                CreditScore=0;
            elif statust==2:
                kl=0;
            elif creditlimit==0:
                credit='ND';
                PurchaseScore=0;
                CreditScore=0;
            elif creditlimit>0 and statust==0:
                credit='LD';
            else:
                kl=0;
            if totalass==0 and longdebt==0 and currliab==0 and grossprofit==0:
                CreditScore=0;
                PurchaseScore=0;
        ###############################################################################
        #######Assigning Rating(A-H) to the Creditscores and Purchase Scores###########
        ###############################################################################
            if 0<=CreditScore<=275:
                CreditRating='H';
            elif 276<=CreditScore<=364:
                CreditRating='G';
            elif 365<=CreditScore<=453:
                CreditRating='F';
            elif 454<=CreditScore<=542:
                CreditRating='E';
            elif 543<=CreditScore<=631:
                CreditRating='D';
            elif 632<=CreditScore<=720:
                CreditRating='C';
            elif 721<=CreditScore<=809:
                CreditRating='B';
            elif CreditScore>810:
                CreditRating='A'
            else:
                CreditRating=''
            if 0<=PurchaseScore<=187:
                PurchaseRating='H';
            elif 188<=PurchaseScore<=249:
                PurchaseRating='G';
            elif 250<=PurchaseScore<=311:
                PurchaseRating='F';
            elif 312<=PurchaseScore<=373:
                PurchaseRating='E';
            elif 374<=PurchaseScore<=435:
                PurchaseRating='D';
            elif 436<=PurchaseScore<=497:
                PurchaseRating='C';
            elif 498<=PurchaseScore<=559:
                PurchaseRating='B';
            elif PurchaseScore>560:
                PurchaseRating='A';
            else:
                PurchaseRating='';
                
            #combinedcreditscore=combcredit+CreditScore
            #combinedpurchasescore=combpurchasee+PurchaseScore
            try:
                if credit=='ND':
                    creditlimits='ND';
                elif credit=='LD':
                    creditlimits='LD';
                else:
                    creditlimits=str(creditlimit)
            except:
                creditlimits=str(creditlimit)

        
                
            records=[str(reg), str(naame),str(CreditRating),str(CreditScore),creditlimits,str(revv)]#,str(combinedcreditscore),str(combinedpurchasescore)]
            
            recds=[str(CreditRating),str(CreditScore),creditlimits,str(revv)]#,str(combinedcreditscore),str(combinedpurchasescore)]
        #################################################################################################################################
        ####  checking if the company scores already exists, if it does then update the table OR insert a new row otherwise##############
        #################################################################################################################################
            
            mycursor=mysql.cursor()
            if updsql==0:
                sql = "INSERT INTO financial_analysis(CompanyNumber, NAME,creditrating, creditscore,creditlimit,revenue) VALUES(%s,%s,%s,%s,%s,%s)"#,combinedcreditscore,combinedpurchasescore)
                mycursor.execute(sql,records)
                mysql.commit()
                mycursor.close()
            else:
                sql="UPDATE financial_analysis SET creditrating=%s,creditscore=%s,creditlimit=%s,revenue=%s  WHERE CompanyNumber='" + reg + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
                mycursor.execute(sql,recds)
                mycursor.close()
            print(records)
            return records
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
#records=regnum('07442456')
#############################################################################################################################################################################
#############UN COMMENT THE CODE TO INSERT INTO TABLE,ALTER THE TABLE, DROP A TABLE OR DROP A COLUMN IN A TABLE############################################################## 
#############################################################################################################################################################################
#        
#    #mycursor.execute("drop table vkingsol_frennsdevelopment.sync_payment_analysis")
#    #mycursor.execute("ALTER TABLE syncpaymentanalysis drop column name")# company_numberY, creditscoreY, creditlimitY, purchasescoreY)")
#    #mycursor.execute("CREATE TABLE sync_payment_analysis (name VARCHAR(255), company_number VARCHAR(255), creditscore VARCHAR(255), creditlimit VARCHAR(255), purchasescore VARCHAR(255))")
#    #mycursor.execute("ALTER TABLE syncpaymentanalysis ADD (name VARCHAR(255), company_number VARCHAR(255), creditscore VARCHAR(255), creditlimit VARCHAR(255), purchasescore VARCHAR(255))")
#        


##################################################################
#######Uncomment this to run from command line####################
##################################################################

#import sys
#arg=sys.argv[1]
#regnum(arg)

####################################################################################################
##Connecting to the server and collecting REGNUMBER of all the companies in the latest year FIRST###
############Note- Change the host value to localhost when running on a local server#################
####################################################################################################
#
#import mysql.connector
#import numpy as np
#import pandas as pd
#
#mysql = mysql.connector.connect(
#      host="144.76.137.232",
#      user="clearsightext",
#      passwd="gR985xi*",
#      database = "clearsight_development"
#      )
##read_years=pd.read_sql('select YEAR from company_ann_reports', con=mysql)
##years=read_years['YEAR']
##total_years=years.drop_duplicates()
##total_years_array=np.array(total_years)
##maximum_year=max(total_years_array)
##minimum_year=min(total_years_array)
#for year in range(2020,2000,-1):
#    years=str(year)
#    data=pd.read_sql('select CompanyNumber from company_ann_reports where YEAR="'+years+'"', con=mysql)
#    reg_number=data['CompanyNumber']
#    reg_number_without_duplicates=reg_number.drop_duplicates().reset_index(drop=True)
#    reg_number_array=np.array(reg_number_without_duplicates)
#    #looping all the companies in the considered year
#    for i in range(0,len(reg_number_array)):
#        regnum(reg_number_array[i])
#mysql.commit()
#mysql.close()

