# generate graph in a certain time period
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"

import datetime
import os

from utilities.draw_line_chart import draw_line_chart
import pandas as pd
import numpy as np

filepath = os.path.realpath(__file__)
dirname = os.path.dirname(filepath)
os.chdir(dirname)


def gen_graph(df, year, month, writer, sheet_name, chart_title, graph_type):
    return_dict = {}
    df = pd.DataFrame(df)
    by = get_by_condition(df, graph_type, year, month)
    result = by.agg({'year': 'first',
                     graph_type: 'first',
                     'value_min': np.min,
                     'value_max': np.max}).reset_index(drop=True)
    value_min = get_value(result, 'value_min')
    value_max = get_value(result, 'value_max')
    time_period = get_time_period(graph_type, result)
    value_mean = []

    for i in range(len(value_min)):
        value_mean.append((value_min[i] + value_max[i]) / 2)

    return_dict[graph_type] = time_period
    return_dict['min'] = value_min
    return_dict['mean'] = value_mean
    return_dict['max'] = value_max

    cat_1 = ['min', 'mean', 'max']
    index_1 = time_period
    multi_iter1 = {'time': index_1}
    for cat in cat_1:
        multi_iter1[cat] = return_dict[cat]
    # sheet_name = site + "_monthly_report"
    draw_line_chart(cat_1, multi_iter1, sheet_name, writer, chart_title, graph_type, 'Connections')
    return return_dict


def get_time_period(graph_type, result):
    time_period = result[graph_type]
    time_period = [int(x) for x in time_period]
    if graph_type=="month":
        time_period = [datetime.date(1900, x, 1).strftime('%b') for x in time_period]
    elif graph_type=="week":
        time_period = [str(x) for x in time_period]
    return time_period


def get_value(result, value_type):
    value = result[value_type]
    value = [np.int32(x) for x in value]
    return value


def get_by_condition(df, graph_type, year, month):
    if graph_type == 'month':
        by = df[df['year'] == year].groupby(['year', graph_type])
    elif graph_type == 'week':
        by = df[df['year'] == year][df['month'] == month].groupby(['year', 'week'])
    else:
        by = df[df['year'] == year][df['month'] == month].groupby(['year', 'day'])
    return by
