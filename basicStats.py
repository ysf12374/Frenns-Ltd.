from dataFrame import Parser
import pandas as pd
import numpy as np
from dbutils import DbUtils
import os
import inspect

pd.options.mode.chained_assignment = None

# prediction next months
def prediction_months(month_list, last_month):
    last_month_index = month_list.index(last_month.lower().title())
    max_index_of_month_list = month_list.index(month_list[-1])
    dif_value = max_index_of_month_list - last_month_index
    next_month_list = []

    if dif_value < 3:
        i = 1
        while i <= 3:
            next_month_index = last_month_index + i
            if next_month_index > max_index_of_month_list:
                next_month_index = next_month_index - max_index_of_month_list - 1
            next_month_list.append(month_list[next_month_index])
            i += 1
    else:
        next_month_list = month_list[last_month_index + 1: last_month_index + 4]

    return next_month_list

# generating values for trend, prediction line drawing
def trend_line_generating(dataframe):
        data_list = dataframe.tolist()
        n = len(data_list)
        x = np.array([i for i in range(len(data_list))])
        y = np.array(data_list)
        m, c = np.polyfit(x, y, 1)
    #    print(m,c)
    
        trend_values = []
        prediction_values = []
        trajectory_values = []
        for i in range(n + 3):
            trajectory_values.append(m*i)
            if i < n:
                t = m * i + c
                trend_values.append(t)
                prediction_values.append(None)
            else:
                p = m * i + c
                prediction_values.append(p)
                trend_values.append(None)
        return trend_values, prediction_values, trajectory_values, m

class UserStats(Parser):

    def __init__(self, frn_number):
        super(self.__class__, self).__init__()
        self.frn = frn_number
        self.month = ['January', 'February', 'March',
                  'April', 'May', 'June',
                  'July', 'August', 'September',
                  'October', 'November', 'December']

        self.prediction_month_value = [None, None, None]

        self.dic_month = {'JANUARY': 'JAN', 'FEBRUARY': 'FEB', 'MARCH': 'MAR', 'APRIL': 'APR', 'MAY': 'MAY', 'JUNE': 'JUN',
                     'JULY': 'JUL', 'AUGUST': 'AUG', 'SEPTEMBER': 'SEP', 'OCTOBER': 'OCT', 'NOVEMBER': 'NOV',
                     'DECEMBER': 'DEC'}
        self.dic_pre_month = {'JANUARY': 'Next_JAN', 'FEBRUARY': 'Next_FEB', 'MARCH': 'Next_MAR', 'APRIL': 'Next_APR', 'MAY': 'Next_MAY', 'JUNE': 'Next_JUN',
                     'JULY': 'Next_JUL', 'AUGUST': 'Next_AUG', 'SEPTEMBER': 'Next_SEP', 'OCTOBER': 'Next_OCT', 'NOVEMBER': 'Next_NOV',
                     'DECEMBER': 'Next_DEC'}
        self.db = DbUtils(frn_number=frn_number)
        self.pwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


    def cashflowNProfit(self):
        cash_flow_df = self.invoiceCSV[self.invoiceCSV.frenns_id == self.frn]
        if cash_flow_df.shape[0] == 0:
            return None
        else:
            # getting dataframe
            revenue = cash_flow_df.iloc[0, 2:]
#            print("revenue",len(revenue))
            cost = cash_flow_df.iloc[1, 2:]
#            print("cost",len(cost))
            cash_flow = revenue - cost
#            print("cash_flow",len(cash_flow))
            profit = (cash_flow / revenue) * 100
#            print("profit",len(profit))

            # calculating trend, prediction line, k value
            cost_trend, cost_prediction, cost_trajectory, cost_trend_k = trend_line_generating(cost)
#            print("cost trend",trend_line_generating(cost))
#            print('\n')
            cash_flow_trend, cash_flow_prediction, cash_flow_trajectory, cash_flow_trend_k = trend_line_generating(cash_flow)
#            print("cash flow trend",trend_line_generating(cash_flow))
            # getting month list including prediction months info
            month_abbreviation_list = [self.dic_month.get(n, n) for n in cash_flow_df.columns.values[2::].tolist()]
            prediction_month_list = prediction_months(self.month, (cash_flow_df.columns.values[2::].tolist()[-1]))
            months = month_abbreviation_list + prediction_month_list
#            print(months,"month",len(months))
            # producing data frame for curve
            ret = {'cash_flow': cash_flow.tolist() + self.prediction_month_value, 'profit': profit.tolist() + self.prediction_month_value,
                   'cost': cost.tolist() + self.prediction_month_value, 'revenue': revenue.tolist() + self.prediction_month_value, 'cost_trend': cost_trend, 'cashflow_trend': cash_flow_trend, 'cost_prediction': cost_prediction, 'cashflow_prediction': cash_flow_prediction}
#            print(ret,"ret",len(ret['cash_flow']))
            cash_flow_profit_graph_df = pd.DataFrame(ret, index=months)
            cash_flow_json_data = cash_flow_profit_graph_df.to_json(orient='index')

            k_values = "{'cost_trend_k': %f, 'cost_flow_k': %f}" % (cost_trend_k, cash_flow_trend_k)
            self.db.save_update_curve_values('cash_flow', cash_flow_json_data, k_values)
            return cash_flow_profit_graph_df

    def revenueNCostIncrease(self):
        cash_flow_df = self.invoiceCSV[self.invoiceCSV.frenns_id == self.frn]
        if cash_flow_df.shape[0] == 0:
            return None
        else:
            # getting data frame
            revenue = cash_flow_df.iloc[0, 2:]
#            print("revenue",len(revenue))
            cost = cash_flow_df.iloc[1, 2:]
#            print("cost",len(cost))
            revenue_increase = (revenue - revenue.shift(1)) / (revenue+1) * 100
#            print("rev1enue_increase",len(revenue_increase))
#            print("cost and  shift\n",cost,"\n",cost.shift(1))
            cost_increase = ((cost - cost.shift(1)) / (cost+1) )* 100
#            print("cost_increase",cost_increase)

            # calculating trend, prediction line, k value
            cost_trend, cost_prediction, cost_trajectory, cost_trend_k = trend_line_generating(cost)
            cast_increase_trend, cast_increase_prediction, cast_increase_trajectory, cast_increase_trend_k = trend_line_generating(cost_increase.dropna())
            revenue_increase_trend, revenue_increase_prediction, revenue_increase_trajectory, revenue_increase_trend_k = trend_line_generating(revenue_increase.dropna())

            revenue_increase_trend.insert(0, None)
            revenue_increase_prediction.insert(0, None)
            cast_increase_trend.insert(0, None)
            cast_increase_prediction.insert(0, None)

            ret = {"costIncrease": cost_increase.tolist() + self.prediction_month_value, "revenueIncrease": revenue_increase.tolist() + self.prediction_month_value, 'cost': cost.tolist() + self.prediction_month_value, 'revenue': revenue.tolist() + self.prediction_month_value, 'cost_trend': cost_trend, 'cost_prediction': cost_prediction, 'cast_increase_trend': cast_increase_trend, 'cast_increase_prediction': cast_increase_prediction, 'revenue_increase_trend': revenue_increase_trend, 'revenue_increase_prediction': revenue_increase_prediction}
            month_abbreviation_list = [self.dic_month.get(n, n) for n in cash_flow_df.columns.values[2::].tolist()]
            prediction_month_list = prediction_months(self.month, (cash_flow_df.columns.values[2::].tolist()[-1]))
            months = month_abbreviation_list + prediction_month_list
#            print(ret,"\n",months)
#            print("ret",len(ret),"months",len(months))
            # producing data frame for graph
            cash_flow_json_graph_df = pd.DataFrame(ret, index=months)
            cash_flow_json_data = cash_flow_json_graph_df.to_json(orient='index')
            k_values = "{'cost_trend_k': %f, 'cast_increase_trend_k': %f, 'revenue_increase_trend_k': %f}" % (cost_trend_k, cast_increase_trend_k, revenue_increase_trend_k)

            self.db.save_update_curve_values('revenue', cash_flow_json_data, k_values)
            return cash_flow_json_graph_df

    def business_statistics(self):
        business_df = self.businessCSV[self.businessCSV.frenns_id == self.frn]
        if business_df.shape[0] == 0:
            return None
        else:

            # getting data frame from csv
            repeat_business = business_df.iloc[1, 2:]
            new_business = business_df.iloc[0, 2:]
            moving_avg_rb = repeat_business.rolling(window=2).mean()
            moving_avg_nb = new_business.rolling(window=2).mean()

            # calculating trend line, prediction line, k value
            repeat_business_trend, repeat_business_prediction, repeat_business_trajectory, repeat_business_trend_k = trend_line_generating(repeat_business)
            new_business_trend, new_business_prediction, new_business_trajectory, new_business_trend_k = trend_line_generating(new_business)
            moving_avg_nb_trend, moving_avg_nb_prediction, moving_avg_nb_trajectory, moving_avg_nb_trend_k = trend_line_generating(moving_avg_nb.dropna())
            moving_avg_rb_trend, moving_avg_rb_prediction, moving_avg_rb_trajectory, moving_avg_rb_trend_k = trend_line_generating(moving_avg_rb.dropna())
            moving_avg_nb_trend.insert(0, None)
            moving_avg_nb_prediction.insert(0, None)
            moving_avg_rb_trend.insert(0, None)
            moving_avg_rb_prediction.insert(0, None)

            zero_trajectory = np.zeros(len(repeat_business_trajectory))

            # business data frame for graph
            ret = {'zero_trajectory': zero_trajectory, 'repeat_business_trajectory': repeat_business_trajectory, 'new_business_trajectory': new_business_trajectory, "repeatBusiness": repeat_business.tolist() + self.prediction_month_value, "movingAvgRB": moving_avg_rb.tolist()+ self.prediction_month_value, "newBusiness": new_business.tolist()+ self.prediction_month_value, "movingAvgNB": moving_avg_nb.tolist()+ self.prediction_month_value, 'repeat_business_trend': repeat_business_trend, 'repeat_business_prediction': repeat_business_prediction, 'new_business_trend':new_business_trend, 'new_business_prediction': new_business_prediction, 'moving_avg_nb_trend': moving_avg_nb_trend, 'moving_avg_rb_trend': moving_avg_rb_trend, 'moving_avg_nb_prediction': moving_avg_nb_prediction, 'moving_avg_rb_prediction': moving_avg_rb_prediction}
            month_abbreviation_list = [self.dic_month.get(n, n) for n in business_df.columns.values[2::].tolist()]
            prediction_month_list = prediction_months(self.month, (business_df.columns.values[2::].tolist()[-1]))
            months = month_abbreviation_list + prediction_month_list
            k_values = "{'repeat_business_trend_k': %f, 'new_business_trend_k': %f, 'moving_avg_nb_trend_k': %f, 'moving_avg_rb_trend_k': %f}" % (repeat_business_trend_k, new_business_trend_k, moving_avg_nb_trend_k, moving_avg_rb_trend_k)
            business_json_graph_df = pd.DataFrame(ret, index=months)
            business_json_data = business_json_graph_df.to_json(orient='index')
            self.db.save_update_curve_values('business', business_json_data, k_values)

            return business_json_graph_df

    def max_min(self):
        self.dateCSV['due_date'] = pd.to_datetime(self.dateCSV.due_date)
        self.dateCSV['issue_date'] = pd.to_datetime(self.dateCSV.issue_date)
        date_df = self.dateCSV[self.dateCSV.frenns_id == self.frn]
        date_df['ETA'] = ((date_df.due_date - date_df.issue_date) / np.timedelta64(1, 'D')).astype(int)

        customer_last_month = ''
        customer_last_month_index = 0
        max_days = np.zeros(12, dtype=int).tolist()
        min_days = np.zeros(12, dtype=int).tolist()

        for i, month in enumerate(self.month):

            month_data = date_df[date_df.start_bidding_time_month == month]
            #if month_data.shape[0] != 0:
            customer_last_month = month
            customer_last_month_index = i
            max_days[i] = month_data.ETA.max()
            min_days[i] = month_data.ETA.min()

        if customer_last_month_index < len(max_days) -1:
            del max_days[customer_last_month_index + 1: len(max_days)]
            del min_days[customer_last_month_index + 1: len(min_days)]

        max_days_df = pd.DataFrame(max_days)
#        print(max_days_df)
        min_days_df = pd.DataFrame(min_days)

        max_days_trend, max_days_prediction, max_days_trajectory, max_days_trend_k = trend_line_generating(max_days_df.iloc[:, 0])
        min_days_trend, min_days_prediction, min_days_trajectory, min_days_trend_k = trend_line_generating(min_days_df.iloc[:, 0])

        days = {'min_days': min_days + self.prediction_month_value, 'max_days': max_days + self.prediction_month_value, 'max_days_trend': max_days_trend, 'max_days_prediction': max_days_prediction, 'min_days_trend': min_days_trend, 'min_days_prediction': min_days_prediction}
        prediction_month_list = prediction_months(self.month, customer_last_month)

        k_values = "{'max_days_trend_k': %f, 'min_days_trend_k': %f}" % (max_days_trend_k, min_days_trend_k)
        self.db.save_update_curve_values('max_min', pd.DataFrame(days, index=[self.dic_month.get(n.upper(), n) for n in self.month[0: customer_last_month_index + 1]] + prediction_month_list).to_json(orient='index'), k_values)

        return pd.DataFrame(days, index=[self.dic_month.get(n.upper(), n) for n in self.month[0: customer_last_month_index + 1]] + prediction_month_list)

    def aging(self):
        self.dateCSV['due_date'] = pd.to_datetime(self.dateCSV.due_date)
        self.dateCSV['issue_date'] = pd.to_datetime(self.dateCSV.issue_date)
        date_df = self.dateCSV[self.dateCSV.frenns_id == self.frn]

        total_number_of_invoices = date_df.shape[0]
        business_aging = np.zeros(12, dtype=int).tolist()

        for i, each in enumerate(self.month):
            month_data = date_df[date_df.start_bidding_time_month == each]
            #if month_data.shape[0] != 0:
            customer_last_month = each
            customer_last_month_index = i
            business_aging[i] = sum(list((month_data.due_date - month_data.issue_date).dt.days))

        if customer_last_month_index < len(business_aging) -1:
            del business_aging[customer_last_month_index + 1: len(business_aging)]

        average_business_aging = (np.array(business_aging) / total_number_of_invoices).tolist()

        average_business_aging_trend, average_business_aging_prediction, average_business_aging_trajectory, average_business_aging_trend_k = trend_line_generating(np.array(business_aging) / total_number_of_invoices)

        zero_trajectory = np.zeros(len(average_business_aging_trajectory))

        ret = {"average_business_aging": average_business_aging + self.prediction_month_value,
               "average_business_aging_trend": average_business_aging_trend,
               "average_business_aging_prediction": average_business_aging_prediction, 'average_business_aging_trajectory': average_business_aging_trajectory, 'zero_trajectory': zero_trajectory}

        prediction_month_list = prediction_months(self.month, customer_last_month)

        k_values = "{'average_business_aging_trend_k': %f}" % average_business_aging_trend_k

        self.db.save_update_curve_values('aging', pd.DataFrame(ret, index=[self.dic_month.get(n.upper(), n) for n in self.month[0: customer_last_month_index + 1]] + prediction_month_list).to_json(orient='index'), k_values)

        return pd.DataFrame(ret, index=[self.dic_month.get(n.upper(), n) for n in self.month[0: customer_last_month_index + 1]] + prediction_month_list)
