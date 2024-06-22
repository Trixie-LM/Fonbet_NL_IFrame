import psycopg2
from data.sensitive_data import SensitiveData


host = SensitiveData.HOST
user = SensitiveData.DB_USER
password = SensitiveData.DB_PASSWORD
db_name = SensitiveData.DB_NAME


# connect to exist database
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True
