# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:38:57 2019

@author: Yousuf
"""
###############################################################################
###############################################################################
###############################################################################

#######     Days Sales in Receivables Index  =====================> DSRI  ##### 
#######     Account Receivable turnover Ratio ====================> artr  #####
#######     Gross Margin Index GMI ===============================> GMI   #####
#######     Asset Quality Index AQI ==============================> AQI   #####
#######     Sales growth Index SGI ===============================> SGI   #####
#######     Depreciation Index DEPI ==============================> DEPI  #####
#######     SGA Expense Index SGAI ===============================> SGAI  #####
#######     Leverage Index LVGI  =================================> LVGI  #####
#######     Total Accruals to Total Assets TATA ==================> TATA  #####
#######     Property, Plant and Equipment PPE  ===================> PPE   #####
#######     Cost of Sales/Cost of Services COS ===================> COS   #####
#######     Selling,General and Administrative Expenses SGA ======> SGA   #####
#######     Amortization  ========================================> AMORT #####
#######     Depreciation  ========================================> DEPR  #####
#######     Profit&Loss Explained ================================> pnl   #####
 
###############################################################################
###############################################################################
###############################################################################
def regnum(reg):
    try:
        import numpy as np
        import pandas as pd
        import mysql.connector
        import math
        import config
        mysql = mysql.connector.connect(
          host=config.HOST,
          user=config.USER,
          passwd=config.PSWD,
          database = config.CLEARSIGHT_NAME
          )
    ##############################################################################################################################
    ##   Selecting all the information available on the company_ann_reports for a particular company number #####################        
    #############################################################################################################################
        df = pd.read_sql('select NAME,YEAR,COS,work_cap,cash,curr_ass,fix_ass,tot_ass,depr_amort,PPE,SGA,Long_term_d,curr_lia,sales,pnl_before_tax,pnl_after_tax,grossprofit from company_ann_reports where CompanyNumber = "' + reg + '" order by YEAR asc', con=mysql)
        pp=pd.read_sql('select CompanyName from fraud_analysis where CompanyNumber ="' + reg + '"', con=mysql)
        if df.empty:
            reg=reg
            naame=''
            dsri='NB' 
            gmi='NB'
            aqi='NB'
            sgi='NB'
            depi='NB'
            sgai='NB'
            lvgi='NB'
            tata='NB'
            M_Score='NB'
            result='NB'
            records=[str(naame),str(reg),str(dsri),str(gmi),str(aqi),str(sgi),str(depi),str(sgai),str(lvgi),str(tata),str(M_Score),result]
            #resultz="Company Not Found "
            #print (resultz)
            return records
        else:
            try:
                updatesql=pp['CompanyName']
                updsql=len(updatesql)
            except:
                updsql=0;
            
            yerr=df['YEAR']
            yr=yerr.as_matrix()
            years=max(yr)
        
            namm=df['NAME']#EXTRACTING NAME
            nm=namm.as_matrix()
            naame=max(nm)
            def minimum(x):
                return min(x)
            def maximum(x):
                return max(x)
            #star=['NAME','YEAR','COS','work_cap','cash','curr_ass','fix_ass','tot_ass','depr_amort','PPE','SGA','Long_term_d','curr_lia','pnl_before_tax','pnl_after_tax','grossprofit']
        
            cos=df['COS']
            cos=cos.as_matrix()
            Cos=cos.sum()
            Cos_min=minimum(cos)
            Cos_max=maximum(cos)
        
            sale=df['sales']
            sale1=sale.as_matrix()
            Sale=sale1.sum()
            Sale_min=minimum(sale1)
            Sale_max=maximum(sale1)
        
            WORK_CAP=df['work_cap']
            WORK_CAP=WORK_CAP.as_matrix()
            work_cap=WORK_CAP.sum()
            
            CASH=df['cash']
            CASH=CASH.as_matrix()
            cash=CASH.sum()
            
            CURR_ASS=df['curr_ass']
            CURR_ASS=CURR_ASS.as_matrix()
            curr_ass=CURR_ASS.sum()
            
            FIX_ASS=df['fix_ass']
            FIX_ASS=FIX_ASS.as_matrix()
            fix_ass=FIX_ASS.sum()
            
            TOT_ASS=df['tot_ass']
            TOT_ASS=TOT_ASS.as_matrix()
            tot_ass=TOT_ASS.sum()
        
            DEPR=df['depr_amort'].astype(int)
            DEPR=DEPR.loc[DEPR<=0]
            DEPR1=DEPR.as_matrix()
            depr=DEPR.sum()
            try:
                AMORT=df['depr_amort'].astype(int)
                AMORT=AMORT.loc[AMORT>=0]
                AMORT1=AMORT.as_matrix()
                amort=AMORT1.sum()
                amort_min=minimum(AMORT1)
                amort_max=maximum(AMORT1)
            except:
                ''''''
            ppe=df['PPE']
            ppe=ppe.as_matrix()
            Ppe=ppe.sum()
        #SGA,Long_term_d,curr_lia,pnl_before_tax,pnl_after_tax,grossprofit
        
            sga=df['SGA']
            sga=sga.as_matrix()
            Sga=sga.sum()
            
            long_debt=df['Long_term_d']
            long_debt=long_debt.as_matrix()
            Long_term_d=long_debt.sum()
        
            curr_l=df['curr_lia']
            curr_l=curr_l.as_matrix()
            curr_lia=curr_l.sum()
        
            GROSSPROFIT=df['curr_lia']
            GROSSPROFIT=GROSSPROFIT.as_matrix()
            grossprofit=GROSSPROFIT.sum()
        
            pnl_aft_tax=df['pnl_after_tax']
            pnl_aft_tax=pnl_aft_tax.as_matrix()
            pnl=pnl_aft_tax.sum()
        
            #def mean(x):
                #x=np.asarray(x)
            #return x.mean()
        ################################################################################
        ##            Calculating the attributes of Beneish Scores       ###############
        ##########  Note- The calculations are adjusted to the database ################
        ################################################################################
        
        #Days Sales in Receivables Index=Number of days in year divided by the artr during the past year 
            Dsri=[]
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            
            for t in range(0,len(yr)):
                def error():
                    dsri=0
                    Dsri.append(dsri)
                    #print("Not Enough Data for D Calculation of {}th year").format(yr[t])
                try:
                    dsri1=float(((TOT_ASS[t])/float(CASH[t])+1.00))
                    dsri2=((TOT_ASS[t+1])/float(CASH[t+1])+1.00)
                    dsri=dsri1/(dsri2+1.00)
                    if math.isnan(dsri):
                        dsri=0
                        Dsri.append(dsri)
                        #print("Not Enough Data for DSRI Calculation of {}th year").format(yr[t])
                    else:
                        Dsri.append(dsri)
                except:
                    error()
            dsri=np.asarray(Dsri).mean()
        #accounts receivable turnover ratio
        #artr=sales[t]/cash[t]
        #dsri=360/artr
        
        #Gross Margin Index GMI
            Gmi=[]
            for t in range(0,len(yr)):
                def error():
                    gmi=0
                    Gmi.append(gmi)
                    #print("Not Enough Data for GMI Calculation of {}th year").format(yr[t])
                try:
                    gmi1=((sale1[t]-cos[t])/(sale1[t]+1))
                    gmi2=((sale1[t+1]-cos[t+1]+1)/(sale1[t+1]+1))
                    gmi=gmi1/(gmi2+1)
                    
                    if math.isnan(gmi):
                        gmi=0
                        Gmi.append(gmi)
                        #print("Not Enough Data for GMI Calculation of {}th year").format(yr[t])
                    else:
                        Gmi.append(gmi)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            gmi=np.asarray(Gmi).mean()
        
        
        #Asset Quality Index AQI
            Aqi=[]
            for t in range(0,len(yr)):
                def error():
                    aqi=0
                    Aqi.append(aqi)
                    #print("Not Enough Data for AQI Calculation of {}th year").format(yr[t])
                try:
                    aqi=(1-(CURR_ASS[t]+ppe[t])/(TOT_ASS[t])+1.00)/((1-(CURR_ASS[t+1]+ppe[t+1])/(TOT_ASS[t+1])+1.00)+1.00)
                    if math.isnan(aqi):
                        aqi=0
                        Aqi.append(aqi)
                        #print("Not Enough Data for AQI Calculation of {}th year").format(yr[t])
                    else:
                        Aqi.append(aqi)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            aqi=np.asarray(Aqi).mean()
        
        #Sales growth Index SGI
            Sgi=[]
            for t in range(0,len(yr)):
                def error():
                        sgi=0
                        Sgi.append(sgi)
                        #print("Not Enough Data for SGI Calculation of {}th year").format(yr[t])
                try:
                    sgi=sale1[t]/sale1[t+1]
                    if math.isnan(sgi):
                        sgi=0
                        Sgi.append(sgi)
                        #print("Not Enough Data for SGI Calculation of {}th year").format(yr[t])
                    else:
                        Sgi.append(sgi)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            sgi=np.asarray(Sgi).mean()
        
        
        #Depreciation Index DEPI
            Depi=[]
            for t in range(0,len(yr)):
                def error():
                    depi=0
                    Depi.append(depi)
                    #print("Not Enough Data for DEPI Calculation of {}th year").format(yr[t])
                try:
                    depi=DEPR1[t]/(DEPR1[t+1]+1.0)
#                    depi2=DEPR1[t+1]/(AMORT1[t+1]+DEPR1[t+1]+1)
#                    depi=depi1/depi2
#                    depi=DEPR1[t]/DEPR1[t+1]
                #depi1=(AMORT1[t-1]/(ppe[t-1]+AMORT1[t-1]+1))/((AMORT1[t]/(ppe[t]+AMORT1[t]+1))+1)
                #depi=(depi+depi1)/2.00
                    if math.isnan(depi):
                        depi=0
                        Depi.append(depi)
                        #print("Not Enough Data for DEPI Calculation of {}th year").format(yr[t])
                    else:
                        Depi.append(depi)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            depi=np.asarray(Depi).mean()
        
        #SGA Expense Index SGAI
            Sgai=[]
            for t in range(0,len(yr)):
                def error():
                    sgai=0
                    Sgai.append(sgai)
                    #print("Not Enough Data for SGAI Calculation of {}th year").format(yr[t])
                try:
                    sgai1=(sga[t]/(sale1[t]+1))
                    sgai2=(sga[t+1]/(sale1[t+1]+1))
                    sgai=sgai1/sgai2


                    if math.isnan(sgai):
                        sgai=0
                        Sgai.append(sgai)
                        #print("Not Enough Data for SGAI Calculation of {}th year").format(yr[t])
                    else:
                        Sgai.append(sgai)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            sgai=np.asarray(Sgai).mean()

        #Leverage Index LVGI
            Lvgi=[]
            for t in range(0,len(yr)):
                def error():
                    lvgi=0
                    Lvgi.append(lvgi)
                    #print("Not Enough Data for LVGI Calculation of {}th year").format(yr[t])
                try:
                    lvgi1=((curr_l[t]+long_debt[t])/(TOT_ASS[t]+1))
                    lvgi2=((curr_l[t+1]+long_debt[t+1])/(TOT_ASS[t+1]+1))
                    lvgi=lvgi1/(lvgi2+1)
                    if math.isnan(lvgi):
                        lvgi=0
                        Lvgi.append(lvgi)
                        #print("Not Enough Data for LVGI Calculation of {}th year").format(yr[t])
                    else:
                        Lvgi.append(lvgi)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            lvgi=np.asarray(Lvgi).mean()
        
        
        #Total Accruals to Total Assets TATA
            Tata=[]
            for t in range(0,len(yr)):
                def error():
                    tata=0
                    Tata.append(tata)
                    #print("Not Enough Data for TATA Calculation of {}th year").format(yr[t])
                try:
                    tata=((pnl_aft_tax[t]+GROSSPROFIT[t])-CASH[t])/(TOT_ASS[t]+1.00)
                    #print(tata)
                    if math.isnan(tata):
                        tata=0
                        Tata.append(tata)
                        #print("Not Enough Data for TATA Calculation of {}th year").format(yr[t])
                    else:
                        Tata.append(tata)
                except:
                    error()
            #print("Ignore Runtime Warning, its because of the empty values in the table")
            tata=np.asarray(Tata).mean()
            #def isNaN(x):
             #   import math
            #return math.isnan(x)

            M_Score=-4.84+(0.920*dsri)+(0.528*gmi)+(0.404*aqi)+(0.892*sgi)+(0.115*depi)-(0.172*sgai)-(0.327*lvgi)+(4.697*tata)

            if math.isinf(M_Score) and M_Score<0:
                M_Score=0;
            elif math.isinf(M_Score) and M_Score>0:
                M_Score=0;
            else:
                M_Score=M_Score
            if sgai==0 or lvgi==0 or tata==0:
                M_Score=-6.065 +(0.823*dsri)+(0.906*gmi)+(0.593*aqi)+(0.717*sgi)+(0.107*depi)

            if math.isinf(M_Score) and M_Score<0:
                M_Score=0;
            elif math.isinf(M_Score) and M_Score>0:
                M_Score=0;
            else:
                M_Score=M_Score
            #sumof=dsri+gmi+aqi+sgi+depi+sgai+lvgi+tata
            if -10<M_Score<=-2.22 and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depr==0 and M_Score!=1.20:
                result='Non Manipulator'
            elif M_Score>-2.22 or M_Score<-11: #and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depr==0 and M_Score!=1.20:
                result='Manipulator'
            elif M_Score==0:
                result='Not Enough Data'
            elif M_Score==0 and dsri==0 and gmi==0 and aqi==0 and sgi==0 and depi==0 and sgai==0 and lvgi==0 and tata==0:
                result='NO DATA'
            else:
                result='Not Enough Data';
            if M_Score==1.20:
                result='NO DATA'
            else:
                k=0;
            #sumof=dsri+gmi+aqi+sgi+depi+sgai+lvgi+tata
#            if M_Score<=-2.22 and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depi!=0 and sgai!=0 and lvgi!=0 and tata!=0:
#                result='Non Manipulator'
#            elif M_Score>-2.22 and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depi!=0 and sgai!=0 and lvgi!=0 and tata!=0:
#                result='Manipulator'
#            elif M_Score==0:
#                result='Not Enough Data'
#            elif M_Score==0 and dsri==0 and gmi==0 and aqi==0 and sgi==0 and depi==0 and sgai==0 and lvgi==0 and tata==0:
#                result=''
#            else:
#                result='Not Enough Data';
#            if M_Score==-4.84:
#                result=''
#                M_Score=0
#            else:
#                k=0;
        #################################################################################################################################
        ####  checking if the company scores already exists, if it does then update the table OR insert a new row otherwise##############
        #################################################################################################################################
            records=[str(naame),str(reg),str(dsri),str(gmi),str(aqi),str(sgi),str(depi),str(sgai),str(lvgi),str(tata),str(M_Score),result]
            recds=[str(dsri),str(gmi),str(aqi),str(sgi),str(depi),str(sgai),str(lvgi),str(tata),str(M_Score),result]

            mycursor=mysql.cursor()
            if updsql==0:
                sql = "INSERT INTO fraud_analysis(CompanyName,CompanyNumber,DSRI,GMI,AQI,SGI,DEPI,SGAI,LVGI,TATA,BeneishMScore,Result) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(sql,records)
                mysql.commit()
                mycursor.close()
                
            else:
                sql="UPDATE fraud_analysis SET DSRI=%s,GMI=%s,AQI=%s,SGI=%s,DEPI=%s,SGAI=%s,LVGI=%s,TATA=%s,BeneishMScore=%s,Result=%s  WHERE CompanyNumber='" + reg + "'"                                       
                mycursor.execute(sql,recds)
                mycursor.close()
                #print("updated {}").format(naame)
            print(records) 
            return records
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
    
      
    
regnum('05723652')
##################################################################
#######Uncomment this to run from command line####################
##################################################################

#==============================================================================
# import sys
# arg=sys.argv[1]
# regnum(arg)
#==============================================================================

####################################################################################################
##Connecting to the server and collecting REGNUMBER of all the companies in the latest year FIRST###
############Note- Change the host value to localhost when running on a local server#################
####################################################################################################

#==============================================================================
# import mysql.connector
# import numpy as np
# import pandas as pd
# import math
# 
# mysql = mysql.connector.connect(
#       host="localhost",
#       user="clearsightext",
#       passwd="gR985xi*",
#       database = "clearsight_development"
#       )
# #read_years=pd.read_sql('select YEAR from company_ann_reports', con=mysql)
# #years=read_years['YEAR']
# #total_years=years.drop_duplicates()
# #total_years_array=np.array(total_years)
# #maximum_year=max(total_years_array)
# #minimum_year=min(total_years_array)
# #print("Ignore Runtime Warning, its because of the empty values in the table")
# for year in range(2020,2000,-1):
#     years=str(year)
#     data=pd.read_sql('select CompanyNumber from company_ann_reports where YEAR="'+years+'"', con=mysql)
#     reg_number=data['CompanyNumber']
#     reg_number_without_duplicates=reg_number.drop_duplicates().reset_index(drop=True)
#     reg_number_array=np.array(reg_number_without_duplicates)
#     #looping all the companies in the considered year
#     for i in range(0,len(reg_number_array)):
#         regnum(reg_number_array[i])
# mysql.commit()
# mysql.close()
# 
# 
# 
#==============================================================================








