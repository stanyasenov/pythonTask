from pprint import pprint

import pandas as pd
from datetime import datetime, timedelta, date


def input_keys(data, keys):

    data = list(data.split(' '))
    columns = []
    for value in data:
        if value in keys:
            columns.append(value)
    return columns


def format_color_groups(df):
    if colored:
        colors = ['blue', 'green', 'yellow']
        current_date = datetime.now()
        x = df.copy()
        factors = list(x['hu'].unique())
        for factor in factors:
            if factor > str(current_date - timedelta(days=90)):
                style = f'background-color: {colors[0]}'
                x.loc[x['hu'] == factor, :] = style
            elif str((current_date - timedelta(days=365))) < factor:
                style = f'background-color: {colors[1]}'
                x.loc[x['hu'] == factor, :] = style
            else:
                style = f'background-color: {colors[2]}'
                x.loc[x['hu'] == factor, :] = style
        return x
    else:
        ''
# def format_colorcode_groups(df):
#     if 'labelIds' in header_labels:
#         x = df.copy()
#         colors = list(x['labelIds'].unique())
#         current_date = datetime.now()
#         factors = list(x['labelIds'].unique())

colored = True
today = date.today()
d1 = today.strftime("%d-%m-%Y")

URL = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'
api_data_as_json = pd.read_json(URL)

csv_data = pd.read_csv('https://raw.githubusercontent.com/VERO-Digital-Solutions/python-task/master/vehicles.csv', delimiter=';',engine='python', on_bad_lines='skip')
combined_data =csv_data.merge(api_data_as_json, how='outer')

filtered_data = combined_data.dropna(subset=['hu'])
filtered_data = filtered_data.sort_values(by='gruppe')
header_labels = ['rnr']
header_labels += input_keys(input(), filtered_data)

rnr_data_only = []

# change range to filtered_data[header_labels]
for rnr in range(20, 23):
    URL_2 = f'https://api.baubuddy.de/dev/index.php/v1/labels/{rnr}'
    labelid_data_as_json = pd.read_json(URL_2)
    colorcode = None
    if 'colorCode' in labelid_data_as_json and 'colorCode' != '':
        colorcode = labelid_data_as_json['colorCode'][0]
    rnr_data_only.append({'rnr':rnr, 'labelIds': colorcode})

rnr_data_only = pd.DataFrame(rnr_data_only)
merged_data = filtered_data.merge(rnr_data_only[['labelIds', 'rnr']], on='rnr', how='left')
merged_data.drop(['labelIds_x'], inplace=True, axis=1)
merged_data.rename(columns={'labelIds_y':'labelIds'}, inplace=True)

styler = merged_data.style

if colored:
    styler.apply(format_color_groups, axis=None)


excelfilename =f'vehicles_{d1}.xlsx'
styler.to_excel(excelfilename, index=False, columns=header_labels)