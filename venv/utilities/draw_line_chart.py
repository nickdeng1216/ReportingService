# generate monthly graph in this year
# __author__ = "Nick Deng"
# __copyright__ = "Copyright@2020, The Reporting Project"
# __license__ = "GPL"
# __version__ = "1.0.1"
# __maintainer__ = "Nick Deng"
# __email__ = "nick@atcnet.com.hk"
# __status__ = "Production"

import pandas as pd


def draw_line_chart(cat, multi_iter, sheet_name, writer, chart_title, x_axis_name, y_axis_name):
    cat_1 = cat
    multi_iter1 = multi_iter

    # Create a Pandas dataframe from the data.
    index_2 = multi_iter1.pop('time')
    df = pd.DataFrame(multi_iter1, index=index_2)
    df = df.reindex(columns=sorted(df.columns))

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    # excel_file = file_name
    sheet_name = sheet_name

    # writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'line'})
    chart.set_title({'name': chart_title})

    # chart.set_title(chart_title)
    # Configure the series of the chart from the dataframe data.
    for i in range(len(cat_1)):
        col = i + 1
        chart.add_series({
            'name': [sheet_name, 0, col],
            'categories': [sheet_name, 1, 0, len(index_2), 0],
            'values': [sheet_name, 1, col, len(index_2), col],
        })

    # Configure the chart axes.
    chart.set_x_axis({'name': x_axis_name})
    chart.set_y_axis({'name': y_axis_name, 'major_gridlines': {'visible': False}})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('G2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    # writer.save()
