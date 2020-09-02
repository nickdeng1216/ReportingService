# get trend data from zabbix via zabbix api
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"

import os
import pandas as pd
from datetime import datetime as dt
from zabbix.get_response import POST
from zabbix.get_auth import get_auth
import datetime

filepath = os.path.realpath(__file__)
dirname = os.path.dirname(filepath)
os.chdir(dirname)

# api path
web_path = "http://www.aisec.cf/aisec/api_jsonrpc.php"


def get_trend_record(itemid, time_from, time_till):
    # get auth after login successfully
    json_string = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "aisec"
        },
        "id": 1
    }
    auth = get_auth(web_path, json_string)

    # get the quantity of the trend of the above item id
    json_string = {
        "jsonrpc": "2.0",
        "method": "trend.get",
        "params": {
            "output": [
                "itemid",
                "clock",
                "num",
                "value_min",
                "value_avg",
                "value_max"
            ],
            "itemids": [
                itemid
            ],
            "countOutput": True
        },
        "auth": auth,
        "id": 1
    }
    # print(POST(web_path, json_string))

    # get the detailed trend data of the above item id
    json_string = {
        "jsonrpc": "2.0",
        "method": "trend.get",
        "params": {
            "output": [
                "itemid",
                "clock",
                "num",
                "value_min",
                "value_avg",
                "value_max"
            ],
            "itemids": [
                itemid
            ],
            "time_from": time_from,
            "time_till": time_till
        },
        "auth": auth,
        "id": 1
    }
    result = POST(web_path, json_string)

    # data process
    df = pd.DataFrame.from_dict(result)

    records = df['result']

    new_records = {}
    key = 0
    for r in records:
        new_records[key] = r
        key = key + 1

    df1 = pd.DataFrame(pd.DataFrame(new_records).T)
    # convert column 'clock' from string to int, and then convert it into date,
    # which cannot be completed directly and need to use lambda
    # df1['clock'] = [int(x) for x in df1['clock']]
    # df1['date'] = [dt.fromtimestamp(x) for x in df1['clock']]
    # combine the above conversion into one
    df1['date'] = [dt.fromtimestamp(x) for x in [int(x) for x in df1['clock']]]
    # convert pandas.tslib.timestamp into date
    df1['date'] = pd.to_datetime(df1['date']).apply(lambda x: x.date())
    df1['year'] = [x.year for x in df1['date']]
    df1['month'] = [x.month for x in df1['date']]
    df1['week'] = [datetime.datetime.fromtimestamp(x).isocalendar()[1] for x in [int(x) for x in df1['clock']]]
    df1['day'] = [x.day for x in df1['date']]
    # df1.to_csv("C:\Project\gen_monthly_wifi_report\gen_monthly_wifi_report.csv")

    return df1
