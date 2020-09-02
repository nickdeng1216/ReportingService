# generate reports
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"
import time
from datetime import datetime as dt
import os
from get_trend_record import get_trend_record
from datetime import timedelta
# from generate_monthly_graph import gen_monthly_graph
# from generate_weekly_graph import gen_weekly_graph
# from generate_daily_graph import gen_daily_graph
from draw_graph import gen_graph
import utilities.excel_operator as pc
import datetime

filepath = os.path.realpath(__file__)
dirname = os.path.dirname(filepath)
os.chdir(dirname)

# set time period
# the corresponding reports should be generated on the first day of this month
# to get the whole year's data to generate monthly report
# and to get the whole month's data to create weekly and daily report
yesterday = dt.now() - timedelta(days=1)
# just for test or special use
# yesterday = dt.strptime("31/07/2020", "%d/%m/%Y")
#########################################################################################
test = False
if not test:
    year = yesterday.year
    month = yesterday.month
    day = yesterday.day
else:
    year = 2020
    month = 8
    day = 31
start_date = "01/01/" + str(year)
time_from = time.mktime(dt.strptime(start_date, "%d/%m/%Y").timetuple())
end_date = str(day) + "/" + str(month) + "/" + str(year)
time_till = time.mktime(dt.strptime(end_date, "%d/%m/%Y").timetuple())

str_month = datetime.date(1900, month, 1).strftime('%b')
excel_file = 'WIFI_Usage_Report_' + str_month + '_' + str(year) + '.xlsx'
writer = pc.open_excel(excel_file)
chart_title = "Connected Users Statistics "


def generate_reports(site, item_id, timestamp_from, timestamp_till, chart_name):
    global df
    df = get_trend_record(item_id, timestamp_from, timestamp_till)
    gen_graph(df, year, month, writer, site + "_monthly_report", chart_name + "(Monthly)", "month")
    gen_graph(df, year, month, writer, site + "_weekly_report", chart_name + "(Weekly)", "week")
    gen_graph(df, year, month, writer, site + "_daily_report", chart_name + "(Daily)", "day")
    # gen_monthly_graph(df, year, site, writer, chart_name + "(Monthly)")
    # gen_weekly_graph(df, year, site, writer, chart_name + "(Weekly)")
    # gen_daily_graph(df, year, month, site, writer, chart_name + "(Daily)")


generate_reports("DWH", 54606, time_from, time_till, chart_title)
generate_reports("LT", 55244, time_from, time_till, chart_title)

pc.close_excel(writer)
