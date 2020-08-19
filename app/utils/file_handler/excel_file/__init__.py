# import pandas
import pandas as pd
import os

# # set file locaton
# file_location = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/data/excelfiles/Mofa 1 Sensoren.xlsx"
#
# file_location = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/data/excelfiles/MoFA1.xlsx"

# # Load spreadsheet
# xl = pd.ExcelFile(file_location)
#
# # print the sheet names
# print(xl.sheet_names)
#
# df1 = xl.parse('Sheet1')
# print(df1.columns.values)
# # print(df1['Behaelter'])
# print(df1.iloc[2])


# import pprint
# for i in range(0, 10):
#     pprint.pprint(df1.iloc[i])

def load_excelfile(filename):
    if not os.path.exists(filename):
        return None
    workbook = pd.ExcelFile(filename)
    try:
        df = workbook.parse(sheet_name=workbook.sheet_names[0])
        return df
    except:
        return None
