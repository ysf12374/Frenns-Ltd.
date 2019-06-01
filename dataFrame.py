import pandas as pd
#from abc import ABC, abstractmethod
#import urllib.request
import os
import inspect
import pymysql.cursors
import warnings
import pymysql
from six.moves import urllib
warnings.filterwarnings('ignore', category=pymysql.Warning)

# getting analysis data
class Parser():#ABC):
    """
    Parses the csv file
    """
    def __init__(self):
        pwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        urllib.request.urlretrieve("https://dev.frenns.com/cron-mail/calculationofinvoice.php", filename=os.path.join(pwd, "..", "..", "data", "business.csv"))
        urllib.request.urlretrieve("https://dev.frenns.com/cron-mail/calculationofrevenueorexpense.php", filename=os.path.join(pwd, "..", "..", "data", "invoicedata.csv"))
        
        self.businessCSV = pd.read_csv(os.path.join(pwd, "..", "..", "data", "business.csv"))
        self.invoiceCSV = pd.read_csv(os.path.join(pwd, "..", "..", "data", "invoicedata.csv"))
        #self.dateCSV = pd.read_csv(os.path.join(pwd, "..", "..", "data", "date.csv"))
#        print(self.businessCSV)

        connection = pymysql.connect(host='localhost',
                             user='vkingsol_demo',
                             password='gUj3z5?9',
                             db='vkingsol_frennsdevelopment',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = r"""SELECT concat('FRN',(100000000+customer_id)) frenns_id ,customer_id,start_bidding_time, MONTHNAME(start_bidding_time) as start_bidding_time_month,YEAR(start_bidding_time) as start_bidding_time_year, issue_date, due_date FROM `marketplace_mpbidding_product` WHERE start_bidding_time !='' ORDER by customer_id asc ,start_bidding_time asc"""
                cursor.execute(sql)
                result = cursor.fetchall()
                self.dateCSV = pd.DataFrame(result, columns=[ 'frenns_id', 'customer_id', 'start_bidding_time', 'start_bidding_time_month', 'start_bidding_time_year', 'issue_date', 'due_date'])
        finally:
            connection.close()

#    @abstractmethod
#    def revenueNCostIncrease(self):
#        pass
#
#    @abstractmethod
#    def cashflowNProfit(self):
#        pass
#
#    @abstractmethod
#    def aging(self):
#        pass
#
#    @abstractmethod
#    def business_statistics(self):
#        pass

    # @abstractmethod
    # def max_min(self):
    #     pass
