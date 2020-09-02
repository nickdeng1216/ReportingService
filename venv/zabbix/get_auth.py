# get authorization string from zabbix
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"

import os
from zabbix.get_response import POST

filepath = os.path.realpath(__file__)
dirname = os.path.dirname(filepath)
os.chdir(dirname)


def get_auth(web_path, json_string):
    return POST(web_path, json_string)['result']
