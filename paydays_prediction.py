import csv, sys, os, pytz, datetime, json, re
import settings, database
#from pyramid.arima import auto_arima
from random import random
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame

def parser(x):
    return datetime.strptime(x,'%Y-%m')

def do_predict(frn_id, year_num, tp_type):
    if tp_type == 'ACCPAY':
        thetype = "supplier"
    elif tp_type == 'ACCREC':
        thetype = "customer"
    else:
        return [0,'invalid request']

    qry_1 = "select DISTINCT company_name from `syncsupplier` where `frenns_id` = '{0}' and `type` = '{1}';".format(frn_id, thetype)
    csr_1 = database.con.cursor()
    csr_1.execute(qry_1)

    for therecord in csr_1:
        try:
            do_the_action(frn_id, year_num, tp_type, thetype, therecord)
        except Exception as e:
            print(e)
            continue
    csr_1.close()

def get_avg_pdays(frn_id, year_num, tp_type, the_sync_ids, the_sync_ids_int):
    qry = "select round( avg( DATEDIFF( CAST( REPLACE(pay_date,'T',' ') as DATE), \
                                        CAST( REPLACE(issue_date,'T',' ') as DATE) \
                                      ) \
                            ) \
                        ) as avg_pay_days from `syncinvoice` where frenns_id = '{0}' and syncsupplier_id in({1}) and `type` = '{2}' and (paid = 'true' or paid = '1') and year(CAST( REPLACE(issue_date,'T',' ') as DATE)) = {3}".format(frn_id, ','.join(the_sync_ids), tp_type, year_num)
    # print(qry)
    cursor3 = database.con.cursor()
    cursor3.execute(qry)
    toreturn = None
    for theavg in cursor3:
        toreturn = theavg[0]
    # print ('==>> avg qry',qry," <<==>>",toreturn)
    return toreturn

def do_the_action(frn_id, year_num, tp_type, thetype, therecord):

    onlyAmt = []
    regex = re.compile('[^a-zA-Z]')
    init_yr, init_mo, init_dt = 1970, 1, None
    last_yr, last_mo, last_dt = 1970, 1, None

    company_name = therecord[0]
    company_name_alnum = regex.sub('', company_name)

    print("predicting for", frn_id, year_num, tp_type, company_name)

    the_sync_ids = []
    the_sync_ids_int = []
    qry_2 = "select syncsupplier_id from `syncsupplier` where `frenns_id` = '{0}' and `company_name` = '{1}';".format(frn_id, company_name)
    csr_2 = database.con.cursor()
    csr_2.execute(qry_2)

    for theinsiderecord in csr_2:
        the_sync_ids.append(str(theinsiderecord[0]))
        the_sync_ids_int.append(int(theinsiderecord[0]))
    csr_2.close()

    compare_date = str(year_num)+'-12-31 23:59:59'
    csvname = frn_id+'_'+str(company_name_alnum)+'_paydates.csv'
    query   = ("SELECT  syncinvoice_id, date(issue_date) as issue_date, date(due_date) as due_date, date(pay_date) as pay_date, COALESCE(DATEDIFF(date(pay_date),date(issue_date)),DATEDIFF(date(NOW()),date(issue_date))) as after_issue_days, DATEDIFF(date(due_date),date(pay_date)) as before_due_days, paid FROM `syncinvoice` where frenns_id = '{0}' and syncsupplier_id in({1}) and `type` = '{2}' and due_date <= '{3}' and DATEDIFF(date('{4}'), date(issue_date)) <= 365 order by issue_date desc;".format(frn_id, ','.join(the_sync_ids), tp_type, compare_date, compare_date))
    # print(query)
    database.cursor.execute(query)

    if database.cursor.rowcount == 0:
        print('NO data')
        return

    if database.cursor.rowcount > 1:
        for (syncinvoice_id, issue_date, due_date, pay_date, after_issue_days, before_due_days, paid) in database.cursor:
            if after_issue_days < 0:
                after_issue_days = 0
            onlyAmt.append([issue_date,after_issue_days])

            #if init_yr == 1970:
            init_yr = issue_date.year
            init_mo = issue_date.month
            init_dt = issue_date
            if last_yr == 1970:
                last_yr = issue_date.year
                last_mo = issue_date.month
                last_dt = issue_date
        onlyAmt.reverse()
        # print(init_mo,init_yr,last_mo,last_yr)
        # convert data to pandas series
        with open(csvname, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(onlyAmt)
        csvFile.close()
        series = read_csv(csvname, header=0, parse_dates=[0], index_col=0, squeeze=True)
        os.remove(csvname)
        # decide sarima attributes
        stepwise_model = auto_arima(series, start_p=1, start_q=1,
                                max_p=3, max_q=3, m=1,
                                start_P=0, seasonal=False,
                                d=1, D=1, trace=False,
                                error_action='ignore',
                                suppress_warnings=True,
                                stepwise=True)
        arima_model = (stepwise_model.order)
        train = series.loc[str(init_dt):str(last_dt)]
    else:
        train = []
    # print(train)

    # do the action
    if(len(train) >= 40):
        stepwise_model.fit(train)
        future_forecast = stepwise_model.predict(n_periods=1)
        if(future_forecast < 0):
            print(frn_id, tp_type, company_name, 'future forecast is negative')
            # return # return [0,'future forecast is negative']
        else:
            query2  = "SELECT id, frenns_id FROM `syncfinancialanalysis` where `frenns_id`='{0}' and acc_type='{1}' and syncsupplier_id={2} and company_type='{3}' and year_number={4};".format(frn_id, tp_type, min(the_sync_ids_int), thetype, year_num)
            # print(query2)
            cursor2 = database.con.cursor()
            cursor2.execute(query2)
            is_record_present = False
            for id, frenns_id in cursor2:
                is_record_present = True
                query = "UPDATE `syncfinancialanalysis` set expected_days = {0} where id ={1};".format(int(future_forecast[0]), id)
            if is_record_present == False:
                query = "INSERT INTO `syncfinancialanalysis`(`frenns_id`, `acc_type`, `company_type`, `expected_days`, `year_number`, `syncsupplier_id`) VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5});".format(frn_id, tp_type, thetype, int(future_forecast[0]), year_num, min(the_sync_ids_int) )
            # print(query)
            database.cursor.execute(query)
            database.con.commit()
            cursor2.close()
            print(frn_id, tp_type, company_name, future_forecast[0])
            # return # return [int(future_forecast[0]),'success']
    else:
        print(frn_id, tp_type, company_name, 'dataset not sufficient')
        # return # return [0,'dataset not sufficient']

    avg_pdays = get_avg_pdays(frn_id, year_num, tp_type, the_sync_ids, the_sync_ids_int)
    if avg_pdays == None:
        avg_pdays = 'null'
    else:
        avg_pdays = int(avg_pdays)

    queryavg1  = "select id, frenns_id FROM `syncfinancialanalysis` where `frenns_id`='{0}' and acc_type='{1}' and syncsupplier_id='{2}' and company_type='{3}' and year_number={4};".format(frn_id, tp_type, min(the_sync_ids_int), thetype, year_num)
    cursoravg1 = database.con.cursor()
    cursoravg2 = database.con.cursor()
    cursoravg1.execute(queryavg1)
    is_avg_present = False
    for theid, thefrenns_id in cursoravg1:
        is_avg_present = True
        queryavg2 = "update syncfinancialanalysis set average_payment_days = {0} where id = {1}".format(avg_pdays, theid)
    if is_avg_present == False:
        queryavg2 = "INSERT into syncfinancialanalysis(syncsupplier_id, frenns_id, acc_type, company_type, average_payment_days, year_number, expected_days) VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, null);".format(min(the_sync_ids_int), frn_id, tp_type, thetype, avg_pdays, year_num)
    # print(queryavg2)
    cursoravg2.execute(queryavg2)
    database.con.commit()
    cursoravg1.close()
    cursoravg2.close()

try:
    frn_id   = sys.argv[1]
    year_num = sys.argv[2]
    tp_type  = sys.argv[3]

    predicted_data = do_predict(frn_id, year_num, tp_type)
    # print(json.dumps(predicted_data))
    database.cursor.close()
    database.con.close()
except Exception as e:
    msg = str(e)
    print("main", e)
    print(json.dumps([0,'something went wrong']))
