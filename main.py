import sys
from basicStats import UserStats
import os
import inspect
import logging
logging.basicConfig(level=logging.DEBUG,filename='plots.log',format='%(name)s - %(levelname)s - %(message)s')#filename='analysis.log',filmode='w'

def main():
    frn_number = sys.argv[1]
    #frn_number = 'FRN100000629'
    pwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    us = UserStats(frn_number, 123)
    try:
        cash_flow_df = us.cashflowNProfit()
        cash_flow_df.to_json(os.path.join(pwd, '..', '..', 'json_data', 'cashFlow_' + frn_number + '.json'), orient='index')
        
    except Exception as e:
        pass
        logging.debug(e)
        #print("1",e)

    try:
        increase_df = us.revenueNCostIncrease()
        increase_df.to_json(os.path.join(pwd, '..', '..', 'json_data', 'increase_' + frn_number + '.json'), orient='index')
    except Exception as e:
        pass
        logging.debug(e)
        #print("2",e)
    try:
        business_df = us.business_statistics()
        business_df.to_json(os.path.join(pwd, '..', '..', 'json_data', 'business_' + frn_number + '.json'), orient='index')
    except Exception as e:
        pass
        logging.debug(e)
        #print("3",e)
    try:
        aging_df = us.aging()
        aging_df.to_json(os.path.join(pwd, '..', '..', 'json_data', 'aging_' + frn_number + '.json'), orient='index')
    except Exception as e:
        pass
        #print("4",e)
    # try:
    #     max_min_df = us.max_min()
    #     max_min_df.to_json(os.path.join(pwd, '..', '..', 'json_data', 'max_min_' + frn_number + '.json'), orient='index')
    # except:
    #     pass


if __name__ == '__main__':
    main()
