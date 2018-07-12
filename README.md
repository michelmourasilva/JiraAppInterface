# Automating data loading to Jira server using Jira Rest API


Configuration file was included in the .gitingnore file, for the creation of a new file just copy the code below to a file that should be called JiraOptions.py

    USERNAME = 'jirauser'
    PASSWORD = 'jirapassword'
    SERVER = 'https://jira.server.com/'
    ORIGIN_FILE = "C:\FILES\origin.CSV"
    ORIGIN_PARSE_DATE = ['date_start', 'date_end']
    ORIGIN_DTYPE = {'technical':object, 'id_technical': object}
    POSTGRESQL_DATABASE = 'database'
    POSTGRESQL_HOSTNAME = '172.0.0.0'
    POSTGRESQL_PORT = 5432
    POSTGRESQL_UID = 'userpostgresql'
    POSTGRESQL_PWS = 'userpostgresql'
    POSTGRESQL_SQL = 'select * from tasks'
    DATE_START_EXTRACT = util.returndatetime()[3]
    DATE_END_EXTRACT = util.returndatetime()[3]