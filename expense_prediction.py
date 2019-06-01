import csv, sys, os, pytz, datetime, json, importlib, json
import settings, database
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from pyramid.arima import auto_arima

importlib.reload(settings)
importlib.reload(database)

def parser(x):
    return datetime.strptime(x,'%Y-%m')

def get_previous_records(frn_id, tp_year, tp_mnth, pseudo = 0, tp_type="ACCPAY"):
    try:

        init_yr   = 1970
        init_mo   = 1
        fquarters = [None,1,4,4,4,7,7,7,10,10,10,1,1]
        csvData   = []
        similar_frns = []

        if pseudo == 0:
            similar_frns.append(str(frn_id))
        else:
            cursor2 = database.con.cursor()
            customer_id  = int(frn_id.replace('FRN',''))-100000000

            get_similar_frn_query = "SELECT entity_id FROM `customer_entity_text` where entity_type_id = 1 and attribute_id = 147 and value like (select value from customer_entity_text where entity_id={0} and entity_type_id = 1 and attribute_id = 147);".format(customer_id)
            cursor2.execute(get_similar_frn_query)

            for records in cursor2:
                similar_frns.append(str("FRN"+str(100000000+records[0])))

        frns_cnt = len(similar_frns)
        query = ("SELECT sum(`outstanding_amount`) as outstanding_amount, CONCAT(YEAR(`creation_date`), CONCAT('-',MONTH(`creation_date`))) as year_and_month, count(distinct frenns_id) as contributors FROM `syncinvoice` where frenns_id in ('{0}') and type = '{1}' group by CONCAT(YEAR(`creation_date`),MONTH(`creation_date`)) order by creation_date ASC;").format("','".join(similar_frns), tp_type)
        # print(query)

        database.cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
        database.cursor.execute(query)

        for (outstanding_amount, year_and_month, contributors) in database.cursor:
            csvData.append([year_and_month, (outstanding_amount/contributors) ])
            if init_yr == 1970:
                init_yr = int(year_and_month.split('-')[0])
                init_mo = int(year_and_month.split('-')[1])
                if init_mo == 12:
                    init_yr = init_yr + 1
                init_mo = fquarters[init_mo]
            else :
                continue

        return [csvData,init_mo,init_yr]
    except Exception as e :
        print("get_previous_records", e)
        return [0,'Database error']

def do_predict(frn_id, tp_year, tp_mnth, last_mo, last_yr, pseudo = 0, tp_type="ACCPAY"):
    try:

        data = get_previous_records(frn_id, tp_year, tp_mnth, pseudo, tp_type)
        csvData = data[0]
        init_mo = data[1]
        init_yr = data[2]

        if len(csvData)==0:
            if pseudo==0:
                return do_predict(frn_id, tp_year, tp_mnth, last_mo, last_yr, 1, tp_type)
            else:
                return [0,"dataset was not sufficient"]

        #<<==convert data to pandas series
        csvname = frn_id+'.csv'
        with open(csvname, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()
        series = read_csv(csvname, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
        os.remove(csvname)
        #==>>

        #<<==decide sarima attributes
        stepwise_model = auto_arima(series, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=3,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
        # print("init_yr",init_yr,"init_mo",init_mo)
        arima_model = (stepwise_model.order)
        sesnl_model = (stepwise_model.seasonal_order)
        train = series.loc[str(init_yr)+'-'+str(init_mo)+'-01':str(last_yr)+'-'+str(last_mo)+'-01']
        #==>>

        #<<==calc min observations needed
        p,d,q,P,D,Q,s = arima_model[0],arima_model[1],arima_model[2],sesnl_model[0],sesnl_model[1],sesnl_model[2],sesnl_model[3]
        observations_needed = d + D*s + max(3*q + 1, 3*Q*s + 1, p, P*s) + 1
        #==>>

        #<<==do the action
        print(train)
        if(len(train) > observations_needed):
            stepwise_model.fit(train)
            future_forecast = stepwise_model.predict(n_periods=1)
            if(future_forecast < 0):
                return [0,'future forecast went negative '+str(future_forecast)]
            else:
                return [round(future_forecast[0],2),'success']
        else:
            if pseudo == 0:
                return do_predict(frn_id, tp_year, tp_mnth, last_mo, last_yr, 1, tp_type)
            else:
                return [0,"dataset was not sufficient"]
        #==>>

    except Exception as e :
        print("do_predict", e)
        return [0,'either dataset not sufficient OR Something else went wrong']

def make_insertion(time_frame, frn_id, tp_type):
    try :

        for record in time_frame :
            year_and_month = record[0].split('-')

            query = ("SELECT count(*) FROM `syncrevenueprediction` WHERE `year_number` ='{0}'  and `month_number`='{1}' and frenns_id='{2}' and acc_type='{3}'".format(year_and_month[0], year_and_month[1], frn_id, tp_type))

            database.cursor.execute(query)
            count = database.cursor.fetchone()

            if count[0] == 0 :
                query = ("INSERT INTO `syncrevenueprediction`(`frenns_id`, `year_number`, `month_number`, `actual_expense`,`is_justified`,`acc_type`) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(frn_id, year_and_month[0], year_and_month[1], record[1], 0, tp_type))
                database.cursor.execute(query)
                database.con.commit()
            else :
                query = ("UPDATE `syncrevenueprediction` SET actual_expense = {0} WHERE `year_number` ='{1}'  and `month_number`='{2}' and frenns_id='{3}' and acc_type = '{4}'".format(record[1], year_and_month[0], year_and_month[1], frn_id, tp_type))
                database.cursor.execute(query)
                database.con.commit()

        return [1,'Success']

    except Exception as e :
        print("make_insertion", e)
        return [0,'Database issue']

def get_past_predicted_data(frn_id, init_mo, init_yr, last_mo, last_yr, tp_type):
    try:

        query = ("SELECT year_number,month_number FROM `syncrevenueprediction` WHERE `predicted_expense` IS NOT NULL and frenns_id='{0}' and `year_number` BETWEEN '{1}' AND '{2}' and acc_type='{3}'".format(frn_id, init_yr, last_yr, tp_type))
        database.cursor.execute(query)
        data = database.cursor.fetchall()
        return data

    except Exception as e :
        print("get_past_predicted_data", e)
        return [0,'Database issue']

try:
    frn_id  = 'FRN100000666'
    tp_year = int(2019)
    tp_mnth = int(1)
    tp_type = 'ACCREC'
#    frn_id  = sys.argv[1]
#    tp_year = int(sys.argv[2])
#    tp_mnth = int(sys.argv[3])
#    tp_type = sys.argv[4]
    last_mo = (tp_mnth - 1) if tp_mnth > 1 else 12
    last_yr = tp_year if last_mo < 12 else (tp_year - 1)

    #<<==insert/update past aggregations in database
    records = get_previous_records(frn_id, tp_year, tp_mnth, 0, tp_type)
    time_frame = records[0]
    make_insertion(time_frame, frn_id, tp_type)
    #==>>

    #<<==make desired prediction
    predicted_data  = do_predict(frn_id, tp_year, tp_mnth, last_mo, last_yr, 0, tp_type)
    predicted_value = predicted_data[0]
    #==>>

    #<<==insert/update desired result in database
    check_query = ("SELECT count(*) as cnt FROM `syncrevenueprediction` WHERE `frenns_id` = '{0}' and `year_number` = '{1}' and `month_number` = '{2}' and `acc_type` = '{3}'".format(frn_id, tp_year, tp_mnth, tp_type))
    database.cursor.execute(check_query)
    thecnt = None
    for (cnt) in database.cursor:
        thecnt = cnt[0]
    if(thecnt):
        query = ("UPDATE `syncrevenueprediction` SET `predicted_expense`='{0}' WHERE `frenns_id` = '{1}' and `year_number` = '{2}' and `month_number` = '{3}' and `acc_type`='{4}'".format(predicted_value, frn_id, tp_year, tp_mnth, tp_type))
    else :
        query = ("INSERT INTO `syncrevenueprediction`(`frenns_id`, `year_number`, `month_number`, `predicted_expense`, `is_justified`, `acc_type`) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(frn_id, tp_year, tp_mnth, predicted_value, 0, tp_type))
    if predicted_value > 0:
        database.cursor.execute(query)
        database.con.commit()
    #==>>

    #<<==update past predictions
    data = get_past_predicted_data(frn_id, records[1], records[2], last_mo, last_yr, tp_type)
    for item in data :
        last_mo = (item[1] - 1) if item[1] > 1 else 12
        last_yr = item[0] if last_mo < 12 else (item[0] - 1)
        prediction_data  = do_predict(frn_id, item[0], item[1], last_mo, last_yr, 0, tp_type)
        predicted_val = prediction_data[0]
        if predicted_val > 0 :
            query = ("UPDATE `syncrevenueprediction` SET `predicted_expense`='{0}' WHERE `frenns_id` = '{1}' and `year_number` = '{2}' and `month_number` = '{3}' and `acc_type` = '{4}'".format(predicted_val, frn_id, item[0], item[1], tp_type))
            database.cursor.execute(query)
            database.con.commit()
    #==>>

    #<<==close db connection
    database.cursor.close()
    database.con.close()
    #==>>
    print(json.dumps(predicted_data))

except Exception as e :
    msg = str(e)
    print("main", e)
    print(json.dumps([0,'something went wrong']))
