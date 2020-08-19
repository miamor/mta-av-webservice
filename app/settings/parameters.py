import os

SQL_SERVER_CONNECTION = {
    'driver': '{ODBC Driver 13 for SQL Server};',
    'server': 'localhost;',
    'database': 'Test',
    'user': 'sa',
    'password': 'BootAI#2018'
}

PARAM_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

LOG_FOLDER = PROJECT_PATH + "/logs/"


class Autotasking:
    pass


class CsvParameters:
    delimiter = '|'
    description_file = "/data/excelfiles/MoFA1.xlsx"


class FileFolderParameters:
    # The full path to the zip files folder, e.g. /home/admin/hemmelrath/zipfiles/
    ZIP_FOLDER_NAME = PROJECT_PATH + "/data/zipfiles/"
    ZIP_EXTRACT_FOLDER_NAME = ''
    CSV_DATA_FOLDER_NAME = PROJECT_PATH+'/data/ai_data/'


    CSV_DELIMITER = ';'
    DIGI_DONE_FILES = 'digi.txt'
    MOFA_DONE_FILES = 'mofa.txt'

    DB_SCRIPTS_FOLDER = PROJECT_PATH + '/db_scripts/'
    DB_SCRIPTS_FOLDER_DIGI = DB_SCRIPTS_FOLDER + '/Digi4.0/'
    DB_SCRIPTS_FOLDER_MOFA = DB_SCRIPTS_FOLDER + "/MoFA/"
    DB_SCRIPTS_FOLDER_HEMMELRATH = DB_SCRIPTS_FOLDER + "/Hemmelrath/"


class DatabaseParameters:
    DB_INFO = dict()

    MYSQL_DB_INFO = dict()

    DIGI_TABLES = ['Item Ledger Entry Type', 'Prod Lot Ouput', 'Feature', 'Item', 'Item Ledger Entry',
                   'Master Data Feature', 'PDC Advice Accumulation', 'Prod_ Order Component', 'Prod_ Order Line',
                   'Prod_ Order Routing Line', 'Prod_ Protocol Header', 'Prod_ Protocol Line', 'Production Order',
                   'QA Feature_Insp_ Meth_ Setup', 'QA Inspection Equipment', 'QA Inspection Method',
                   'QA Inspection Order Header', 'QA Inspection Order Line']

    MOFA_TABLES = ['MoFA', 'FG', 'Behaelter', 'Sensor', 'Sensor_Behaelter', 'Behaelter_Data','MOFA1_A9_Data', 'MOFA1_B1_Data', 'MOFA1_B2_Data', 'MOFA1_B3_Data', 'MOFA1_B4_Data', 'MOFA1_H1_Data', 'MOFA1_H2_Data', 'MOFA1_H3_Data', 'MOFA1_H4_Data', 'MOFA1_M1_Data', 'MOFA1_M2_Data', 'MOFA1_M3_Data', 'MOFA1_M4_Data', 'MOFA1_M5_Data', 'MOFA1_M6_Data', 'MOFA1_M7_Data', 'MOFA1_M8_Data', 'MOFA1_S1_Data', 'MOFA1_S2_Data', 'MOFA1_ST1_Data', 'MOFA1_ST2_Data', 'MOFA1_ST3_Data', 'MOFA1_ST4_Data', 'MOFA1_ST5_Data', 'MOFA1_ST6_Data', 'MOFA1_ST7_Data', 'MOFA1_ST8_Data']


class SqlConnectionParameter:
    class MSSQLParameters:
        driver = '{ODBC Driver 13 for SQL Server}'
        server = 'localhost'  # 'sv1.vn.boot.ai'  # 'localhost'
        database = 'Digi4.0'  # The default database to call sql class
        database_digi = 'Digi4.0'  # 'Test"
        database_mofa = 'MoFA'
        database_hemm = 'Hemmelrath'
        database_hemm_ai = 'Hemmelrath.AI'
        uid = 'sa'
        pwd = 'BootAI#2018'  # 'c8SRc9W4Z9VEFaEV'  # '1507'

    class MySQLParameters:
        pass

    class SqlLiteParameters:
        pass


class Types:
    type_text = 'text'
    type_acknowledgment = 'acknowledgment'
    type_mobile = 'mobile'
    type_threat = 'threat'
    type_malware = 'capture'
    type_image = 'image'
    type_video = 'video'
    type_audio = 'audio'

# if __name__ == '__main__':
#     print(ZIP_FOLDER_NAME)

# print(SqlConnectionParameter.MSSQLParameters.database)
