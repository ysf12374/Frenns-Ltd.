import pymysql.cursors
import pymysql
import os
import inspect
import json


def getConnection():
    connection = pymysql.connect(host='localhost',
        user='vkingsol_demo',
        password='gUj3z5?9',
        db='vkingsol_frennsdevelopment',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

class DbUtils:

    def __init__(self, frn_number):
        self.frn = frn_number
        self.month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    def save_update_curve_values(self, table_name, json_data, k_values):
        table_name = 'py_' + table_name
        connection = getConnection()
        # converting from json_data to dict
        data_list = json.loads(json_data)

        # check_sql
        check_sql_param = ()
        check_sql_param = check_sql_param + (table_name, self.frn)
        check_sql = "SELECT * FROM %s where customer_id = '%s' " % check_sql_param

        # insert_sql
        insert_params = ()
        update_params = ()
        insert_params = insert_params + (table_name, self.frn)
        update_params = update_params + (table_name,)
        for month in self.month_list:
            if month in data_list:
                insert_params = insert_params + (data_list[month], )
                update_params = update_params + (data_list[month], )

            else:
                insert_params = insert_params + (None, )
                update_params = update_params + (None, )

        insert_params = insert_params + (data_list[list(data_list.keys())[-3]], data_list[list(data_list.keys())[-2]], data_list[list(data_list.keys())[-1]], k_values)
        update_params = update_params + (data_list[list(data_list.keys())[-3]], data_list[list(data_list.keys())[-2]], data_list[list(data_list.keys())[-1]], k_values, self.frn)
        insert_sql = 'insert into %s( customer_id, january, february, march, april, may, jun, july, august, september, october, november, december, first_prediction_month, second_prediction_month, third_prediction_month, k_values) values("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s", "%s", "%s")' % insert_params

        update_sql = 'update %s set january="%s", february="%s", march="%s", april="%s", may="%s", jun="%s", july="%s", august="%s", september="%s", october="%s", november="%s", december="%s", first_prediction_month="%s", second_prediction_month="%s", third_prediction_month="%s", k_values="%s" where customer_id = "%s"' % update_params

        try:
            with connection.cursor() as cursor:
                cursor.execute(check_sql)
                result = cursor.fetchone()
                if result:
                    cursor.execute(update_sql)
                    connection.commit()
                else:
                    cursor.execute(insert_sql)
                    connection.commit()

        except pymysql.IntegrityError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        except pymysql.InternalError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        except Exception  as e:
            print("Error : ", ','.join(e.args))

        finally:
            connection.close()
