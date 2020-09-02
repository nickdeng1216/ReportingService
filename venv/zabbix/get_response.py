# post JSON to zabbix server via api
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"
import requests


def POST(web_path, json_string):
    return requests.post(web_path, json=json_string).json()
