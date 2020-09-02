# process date and excel writer
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"

import pandas as pd


def open_excel(excel_file):
    return pd.ExcelWriter(excel_file, engine='xlsxwriter')


def close_excel(writer):
    writer.save()
