import psycopg2
import JiraOptions
import pandas as pd


def postgresql_connection():
    connection_string = 'host={0} port={1} dbname={2} user={3} password={4}'\
        .format(JiraOptions.POSTGRESQL_HOSTNAME,
                JiraOptions.POSTGRESQL_PORT,
                JiraOptions.POSTGRESQL_DATABASE,
                JiraOptions.POSTGRESQL_UID,
                JiraOptions.POSTGRESQL_PWS)
    return psycopg2.connect(connection_string)


class data_frame_mapper(object):
    def __init__(self, splitter='|', encoding='ISO-8859', parse_date=None, day_first=True,
                 origin='POSTGRESQL', date_start_export=JiraOptions.DATE_START_EXTRACT,
                 date_end_export=JiraOptions.DATE_END_EXTRACT):
        self.splitter = splitter
        self.encoding = encoding
        self.parse_date = parse_date
        self.day_fist = day_first
        self.date_start_export = date_start_export
        self.date_end_export = date_end_export

        if origin == 'POSTGRESQL':
            self.data_frame = self.get_data_frame_database()
        elif origin == 'CSV':
            self.data_frame = self.get_data_frame_database()

    def get_data_frame_csv(self):
        return pd.read_csv(JiraOptions.ORIGIN_FILE, sep=self.splitter, encoding=self.encoding,
                           parse_dates=JiraOptions.ORIGIN_DTYPE, dayfirst=self.day_fist)

    def get_data_frame_database(self):
        return pd.read_sql_query(JiraOptions.POSTGRESQL_SQL.format(self.date_start_export, self.date_end_export),
                                 postgresql_connection())

