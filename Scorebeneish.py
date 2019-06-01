# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:20:14 2019

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
#NAME,YEAR,work_cap,cash,curr_ass,fix_ass,tot_ass,depr_amort,PPE,Long_term_d,curr_lia,pnl_before_tax,pnl_after_tax,grossprofit

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
            database = config.FRENNS_NAME
          )
        data=pd.read_sql('select * from syncreport_pl where frenns_id ="' + reg + '"' , con=mysql)
        all_data=data['account_name']
        all_data_without=all_data.drop_duplicates().reset_index(drop=True)
        pp=pd.read_sql('select * from syncfraudanalysis where frenns_id ="' + reg + '" and area="Beneish-M Score" ', con=mysql)
        try:
            updatesql=pp.loc[pp['area']=='Beneish-M Score']
            updatesql=updatesql['frenns_id']
            updsql=len(updatesql)
        except:
            updsql=0;
        values={'value':0}
        data=data.fillna(value=values)
    #df = pd.read_sql('select * from syncreport_pl where frenns_id = "FRN100000534" ' , con=mysql)#where frenns_id = "FRN100000414"
    #acctype=df['account_type']
    #detacctyp=df['detail_acc_type']
    #frenns_beneish=df['frenns_beneish_cat']
    #acc_without_duplicates=acctype.drop_duplicates().reset_index(drop=True)
    #det_without=detacctyp.drop_duplicates().reset_index(drop=True)
    #frenns_beneish_without=frenns_beneish.drop_duplicates().reset_index(drop=True)
    #
    #empty=df.loc[df['account_type']==''].reset_index(drop=True)
    #empty_acc_names=empty['account_name'].drop_duplicates().reset_index(drop=True)
        def vals(names):
            n=names
            n=data.loc[data['account_name']==names].reset_index(drop=True)['value'].astype(float)
            try:
                n1=max(n)
            except:
                n1=0
            try:
                n2=min(n)
            except:
                n2=0
            if n1==n2:
                n2=0;
            return n1,n2
        def maximum(x):
            try: 
                return max(x)
            except:
                return 0
        def minimum(x):
            try: 
                return min(x)
            except:
                return 0
        curr_ass1=vals('Suspense Account')
        turnover=vals('Sales Type')
        expense1=vals('Outgoing Type')
        expense2=vals('Bank Transaction Type')
        cash1=vals('Cash and cash equivalents')
        receivable=vals('Accounts Receivable (A/R)')
        currliab1=vals('Tax Payable')
        pnl1=vals('Retained Earnings')
        sales=vals('Sales')
        sga=vals('Amortisation expense')
        cash2=vals('Bank USD')
        curr_ass2=vals('Allowance for bad debt')
        curr_ass3=vals('Available for sale assets (short-term)')
        curr_ass4=vals('Inventory')
        curr_ass5=vals('Inventory Asset')
        curr_ass6=vals('Prepaid expenses')
        curr_ass7=vals('Uncategorised Asset')
        depr=vals('Accumulated depreciation on property, plant and equipment')
        ppe=vals('Property, plant and equipment')
        asset1=vals('Assets held for sale')
        asset2=vals('Deferred tax assets')
        asset3=vals('Goodwill')
        asset4=vals('Intangibles')
        asset5=vals('Long-Term Investments')
        curr_ass8=vals('Accrued liabilities')
        curr_ass9=vals('Dividends payable')
        currliab2=vals('Income tax payable')
        currliab3=vals('Payroll Clearing')
        currliab4=vals('Payroll liabilities')
        currliab5=vals('Short-term debit')
        currliab6=vals('Tax Suspense')
        currliab7=vals('Accrued holiday payable')
        currliab8=vals('Accrued non-current liabilities')
        currliab9=vals('Liabilities related to assets held for sale')
        currliab10=vals('Long-term debt')
        ownereq1=vals('Dividend disbursed')
        ownereq2=vals('Equity in earnings of subsidiaries')
        ownereq3=vals('Opening Balance Equity')
        ownereq4=vals('Other comprehensive income')
        ownereq5=vals('Share capital')
        income1=vals('Billable Expense Income')
        income2=vals('Revenue - General')
        income3=vals('Sales - retail')
        income4=vals('Sales - wholesale')
        income5=vals('Sales of Product Income')
        income6=vals('Unapplied Cash Payment Income')
        income7=vals('Uncategorised Income')
        cos1=vals('Change in inventory - COS')
        cos2=vals('Cost of sales')
        cos3=vals('Direct labour - COS')
        cos4=vals('Discounts given - COS')
        cos5=vals('Freight and delivery - COS')
        cos6=vals('Materials - COS')
        cos7=vals('Other - COS')
        cos8=vals('Overhead - COS')
        cos9=vals('Subcontractors - COS')
        debt1=vals('Bad debts')
        expense3=vals('Bank charges')
        expense4=vals('Commissions and fees')
        expense5=vals('Dues and subscriptions')
        expense6=vals('Equipment rental')
        expense7=vals('Income tax expense')
        expense8=vals('Insurance - Disability')
        expense9=vals('Insurance - General')
        expense10=vals('Insurance - Liability')
        expense11=vals('Interest expense')
        expense12=vals('Legal and professional fees')
        expense13=vals('Loss on discontinued operations, net of tax')
        expense14=vals('Legal and professional fees')
        expense15=vals('Management compensation')
        expense16=vals('Meals and entertainment')
        expense17=vals('Office expenses')
        expense18=vals('Other general and administrative expenses')
        expense19=vals('Other selling expenses')
        expense20=vals('Other Types of Expenses-Advertising Expenses')
        expense21=vals('Payroll Expenses')
        expense22=vals('Rent or lease payments')
        expense23=vals('Repairs and Maintenance')
        expense24=vals('Shipping and delivery expense')
        expense25=vals('Stationery and printing')
        expense26=vals('Supplies')
        expense27=vals('Travel expenses - general and admin expenses')
        expense28=vals('Travel expenses - selling expenses')
        expense29=vals('Uncategorised Expense')
        expense30=vals('Utilities')
        expense31=vals('Wage expenses')
        expense32=vals('Supplies')
        income8=vals('Dividend income')
        income9=vals('Interest income')
        income10=vals('Loss on disposal of assets')
        income11=vals('Other operating income (expenses)')
        income12=vals('Unrealised loss on securities, net of tax')
        income13=vals('income')
        income14=vals('income')
        income15=vals('income')
        expense33=vals('Other Expense')
        expense34=vals('Reconciliation Discrepancies')
        
        
        expense_max=[expense1[0],expense2[0],expense3[0],expense4[0],expense5[0],expense6[0],expense7[0],expense8[0],expense9[0],expense10[0],expense11[0],expense12[0],expense13[0],expense14[0],expense15[0],expense16[0],expense17[0],expense18[0],expense19[0],expense20[0],expense21[0],expense22[0],expense23[0],expense24[0],expense25[0],expense26[0],expense27[0],expense28[0],expense29[0],expense30[0],expense31[0],expense32[0],expense33[0],expense34[0]]
        expense_min=[expense1[1],expense2[1],expense3[1],expense4[1],expense5[1],expense6[1],expense7[1],expense8[1],expense9[1],expense11[1],expense11[1],expense12[1],expense13[1],expense14[1],expense15[1],expense16[1],expense17[1],expense18[1],expense19[1],expense21[1],expense21[1],expense22[1],expense23[1],expense24[1],expense25[1],expense26[1],expense27[1],expense28[1],expense29[1],expense31[1],expense31[1],expense32[1],expense33[1],expense34[1]]
        expense_t=[item for item in expense_max if item>=0]
        expense_t_temp=[abs(item) for item in expense_min if item<0]
        expense_t=expense_t+expense_t_temp
        expense_t_1=[item for item in expense_min if item>=0]
        
        
        current_assets_max=[curr_ass1[0],curr_ass2[0],curr_ass3[0],curr_ass4[0],curr_ass5[0],curr_ass6[0],curr_ass7[0],curr_ass8[0],curr_ass9[0]]
        current_assets_min=[curr_ass1[1],curr_ass2[1],curr_ass3[1],curr_ass4[1],curr_ass5[1],curr_ass6[1],curr_ass7[1],curr_ass8[1],curr_ass9[1]]
        cash_t=[cash1[0],cash2[0]]
        cash_t_1=[cash1[1],cash2[1]]
        for x in cash_t_1:
            if x<0:
                cash_t_1.remove(x)
        currliab_t=[currliab1[0],currliab2[0],currliab3[0],currliab4[0],currliab5[0],currliab6[0],currliab7[0],currliab8[0],currliab9[0],currliab10[0]]
        currliab_t_1=[currliab1[1],currliab2[1],currliab3[1],currliab4[1],currliab5[1],currliab6[1],currliab7[1],currliab8[1],currliab9[1],currliab10[1]]
        for x in currliab_t_1:
            if x<0:
                currliab_t_1.remove(x)
        turnover_t=[turnover[0]]
        turnover_t_1=[turnover[1]]
        receivable_t=[receivable[0]]
        receivable_t_1=[receivable[1]]
        pnl_t=[pnl1[0]]
        pnl_t_1=[pnl1[1]]
        sales_t=[sales[0],turnover[0]]
        sales_t_1=[sales[1],turnover[1]]
        sga_t=[sga[0],expense10[0],expense11[0],expense12[0],expense13[0],expense14[0],expense15[0],expense16[0],expense17[0],expense18[0],expense19[0],expense20[0],expense21[0],expense22[0],expense23[0],expense24[0],expense25[0],expense26[0],expense27[0],expense28[0],expense29[0],expense30[0],expense31[0],expense32[0]]
        sga_t_1=[sga[1],expense10[1],expense11[1],expense12[1],expense13[1],expense14[1],expense15[1],expense16[1],expense17[1],expense18[1],expense19[1],expense20[1],expense21[1],expense22[1],expense23[1],expense24[1],expense25[1],expense26[1],expense27[1],expense28[1],expense29[1],expense30[1],expense31[1],expense32[1]]
        curr_ass_t=[curr_ass1[0],curr_ass2[0],curr_ass3[0],curr_ass4[0],curr_ass5[0],curr_ass6[0],curr_ass7[0],curr_ass8[0],curr_ass9[0]]
        curr_ass_t_1=[curr_ass1[1],curr_ass2[1],curr_ass3[1],curr_ass4[1],curr_ass5[1],curr_ass6[1],curr_ass7[1],curr_ass8[0],curr_ass9[0]]
        fix_ass_t=[asset1[0],asset2[0],asset3[0],asset4[0],asset5[0]]
        fix_ass_t_1=[asset1[1],asset2[1],asset3[1],asset4[1],asset5[1]]
        ownereq_t=[ownereq1[0],ownereq2[0],ownereq3[0],ownereq4[0],ownereq5[0]]
        ownereq_t_1=[ownereq1[1],ownereq2[1],ownereq3[1],ownereq4[1],ownereq5[1]]
        income_t=[income1[0],income2[0],income3[0],income4[0],income5[0],income6[0],income7[0],income8[0],income9[0],income10[0],income11[0],income12[0],income13[0],income14[0],income15[0]]
        income_t_1=[income1[1],income2[1],income3[1],income4[1],income5[1],income6[1],income7[1],income8[1],income9[1],income11[1],income11[1],income12[1],income13[1],income14[1],income15[1]]
        depr_t=[depr[0]]
        depr_t_1=[depr[1]]
        ppe_t=[ppe[0]]
        ppe_t_1=[ppe[1]]
        cos_t=[cos1[0],cos2[0],cos3[0],cos4[0],cos5[0],cos6[0],cos7[0],cos8[0],cos9[0]]
        cos_t_1=[cos1[1],cos2[1],cos3[1],cos4[1],cos5[1],cos6[1],cos7[1],cos8[1],cos9[1]]
        debt_t=[debt1[0]]
        debt_t_1=[debt1[1]]
        
        total_asset_t=sum(current_assets_max)+sum(fix_ass_t)
        total_asset_t_1=sum(current_assets_min)+sum(fix_ass_t_1)
        revenues_t=sum(receivable_t)+sum(income_t)
        revenues_t_1=sum(receivable_t_1)+sum(income_t_1)
        liability_t=sum(currliab_t)
        liability_t_1=sum(currliab_t_1)
        grossprof_t=revenues_t-sum(cos_t)
        grossprof_t_1=revenues_t_1-sum(cos_t_1)
        
        
        artr=((total_asset_t)/(float(total_asset_t_1)+1.00))
        
        if math.isinf(artr):
            artr=0;
        if artr==0:
            dsri=360.00/(float(artr)+60.00)
        else:
            dsri=360.00/(float(artr)+1.00)
        if math.isinf(dsri):
            dsri=0.0;
    
        gmi=((sum(sales_t)-sum(cos_t))/(sum(sales_t)+1.00))/((sum(sales_t_1)-sum(cos_t_1))/(sum(sales_t_1)+1.00)+1.00)
        if math.isinf(gmi):
            gmi=0.0;
    
        aqi1=(1-(sum(current_assets_max)+sum(ppe_t))/(total_asset_t+1.00))
        aqi2=((1-(sum(current_assets_min)+sum(ppe_t_1))/(total_asset_t_1+1.00)))
        aqi=aqi1/(aqi2+2.00)
        if math.isinf(aqi):
            aqi=0.0;
            
        sgi=(sum(sales_t_1))/(sum(sales_t)+1.00)
        if math.isinf(sgi):
            sgi=0.0;
        depi1=((sum(depr_t)/(sum(ppe_t)+sum(depr_t)+1.00)))
        depi2=(sum(depr_t_1)/(sum(ppe_t_1)+sum(depr_t_1)+1.00))
        depi=depi1/(depi2+1.00)
        if math.isinf(depi):
            depi=0.0;
    
        sgai=(sum(sga_t)/(sum(sales_t)+1.00))/(sum(sga_t_1)/(sum(sales_t_1)+1.00)+1.00)
        if math.isinf(sgai):
            sgai=0.0;
    
        lvgi1=(((liability_t_1)+sum(debt_t_1))/(total_asset_t+1.00))
        lvgi2=(((liability_t)+sum(debt_t))/(total_asset_t_1+1.00)+1.00)
        #print("lvgi",lvgi1,lvgi2)
        lvgi=lvgi1/(lvgi2+1.00)
        if math.isinf(lvgi):
            lvgi=0.0;
    
        tata=((sum(pnl_t_1)+grossprof_t_1)-sum(cash_t_1))/(total_asset_t+1.00)
        if math.isinf(tata):
            tata=0.0;
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
        #print(dsri,gmi,aqi,sgi,depi,sgai,lvgi,tata)
        if M_Score<=-2.22 and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depi!=0 and M_Score!=1.20:
            result='Non Manipulator'
        elif M_Score>-2.22 and dsri!=0 and gmi!=0 and aqi!=0 and sgi!=0 and depi!=0 and M_Score!=1.20:
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
        #frennsid=reg
        area='Beneish-M Score'
        period='year'
        datefrom=pd.to_numeric(min(data.date_from.astype(str).str[:4]))
        datesto=pd.to_numeric(min(data.date_to.astype(str).str[:4]))
        datefrom=str(datesto)+"-01-01"
        dateto=str(datesto)+"-12-31"
        anomaly='<-2.22'
        
            
    #################################################################################################################################
    ####  checking if the company scores already exists, if it does then update the table OR insert a new row otherwise##############
    #################################################################################################################################
        records=[str(reg),area,period,str(datefrom),str(dateto),str(M_Score),anomaly,result]
        recds=[str(datefrom),str(dateto),str(M_Score),result]
        try:
            mycursor=mysql.cursor()
            if updsql==0:
                sql = "INSERT INTO syncfraudanalysis(frenns_id,area,period,date_from,date_to,value,anomaly,decision) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(sql,records)
                mysql.commit()
                mycursor.close()
                print(records) 
                
            else:
                sql="UPDATE syncfraudanalysis SET date_from=%s,date_to=%s,value=%s,decision=%s  WHERE frenns_id='" + reg + "' and area='Beneish-M Score'"                                       
                mycursor.execute(sql,recds)
                mycursor.close()
                print("updated",recds)
                
                
        except:
            ''''''        
        return records
    except Exception as e:
        print(e)
        res="Executed with some errors"
        return res
        
#regnum('FRN100000667')
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
#       host="144.76.137.232",
#       user="vkingsolextadmin",
#       passwd="bXvg408&",
#       database = "vkingsol_frennsdevelopment"
#       )
# #read_years=pd.read_sql('select YEAR from company_ann_reports', con=mysql)
# #years=read_years['YEAR']
# #total_years=years.drop_duplicates()
# #total_years_array=np.array(total_years)
# #maximum_year=max(total_years_array)
# #minimum_year=min(total_years_array)
# print("Ignore Runtime Warning, its because of the empty values in the table")
# dx=pd.read_sql('select frenns_id from syncreport_pl', con=mysql)
# reg_number=dx['frenns_id']
# reg_number_without_duplicates=reg_number.drop_duplicates().reset_index(drop=True)
# reg_number_array=np.array(reg_number_without_duplicates)
#     #looping all the companies in the considered year#
# try:
#     for i in range(0,len(reg_number_array)):
#         regnum(reg_number_array[i])
# except:
#     mysql.commit()
#     mysql.close()
# mysql.commit()
# mysql.close()
#==============================================================================

