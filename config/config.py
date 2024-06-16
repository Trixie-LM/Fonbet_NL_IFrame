import psycopg2
from data.sensitive_data import sensitive_data


host = sensitive_data.HOST
user = sensitive_data.DB_USER
password = sensitive_data.DB_PASSWORD
db_name = sensitive_data.DB_NAME


# connect to exist database
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True
