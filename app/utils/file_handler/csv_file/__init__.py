import csv
import os
import pandas

from app.settings.parameters import CsvParameters

delim = CsvParameters.delimiter


def read_csv_file_to_list(filename):
    """
    Try to read a csv file to list of data.

    :param filename: A csv file name.

    :return: A list of data.
    """
    data = list()
    try:
        # df = DataFrame.from_csv(path=filename, sep=';') #pandas.read_csv(filename)
        with open(filename, 'r') as csfile:
            df = csfile.read().split('\n')
            df = [x.strip('\n') for x in df]
            for i in range(0, len(df)):
                row = df[i]
                row = row.rstrip()
                if not row:
                    pass
                elif row in ['\n', '\r\n', '']:
                    pass
                elif row.__eq__(''):
                    pass
                else:
                    data.append(row)
    except Exception as e:
        data = None
        print(e.__str__())
    return data


def read_csv_file_to_df(filename, encode=None, delimiter = None):
    """Read data from csv file to dataframe.

    :param filename: The csv file name.

    :return: A DataFrame of data.
    """
    if not filename:
        raise Exception("The " + filename.__str__ + " doest not exist. Please check again.")
    if not os.path.isfile(filename):
        raise Exception("File doest not exist. Please check again.")
    # df = list()
    if delimiter is not None:
        delim = delimiter
    try:
        if encode:
            # df = DataFrame.from_csv(path=filename, sep=delim, encoding=encode)  # pandas.read_csv(filename)
            df = pandas.read_csv(filepath_or_buffer=filename, sep=delim, encoding=encode, dtype=object)
        else:
            # df = DataFrame.from_csv(path=filename, sep=delim)
            df = pandas.read_csv(filepath_or_buffer=filename, sep=delim,dtype=object)
    except Exception as e:
        df = None
        print(e.__str__())
    return df


def read_csv(filename):
    """Read data from csv file using csv built-in module.

    :param filename: The csv file name, and it must not be null.

    :return:
    """
    if not filename:
        raise Exception("The " + str(filename) + " does not exist. Please check again.")
    if not os.path.isfile(filename):
        raise Exception("File does not exist. Please check again")
    with open(filename) as csvfile:
        csv_data = csv.reader(csvfile, delimeter=delim)
    return csv_data

def filter_df(filter_field, max_value, df):
    df = df[df[filter_field] >= str(max_value)]
    return df

if __name__ == '__main__':
    filename = os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))) + "/data/zipfiles/Digi4_20180906_045310/Prod_ Order Routing Line.csv"
    print(filename)
    df = read_csv_file_to_df(filename)
    print(df.head())
    print(df.columns)
    print(type(df))
    print(len(df))
    # print(list(df))
    filter_field = 'Starting Date'
    max_value = '2018-10-18 00:00:00.000'
    filterdf = filter_df(filter_field=filter_field, max_value=max_value, df=df)
    print(len(filterdf))
