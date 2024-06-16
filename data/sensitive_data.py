import os
from dotenv import load_dotenv

load_dotenv()


class SensitiveData:

    # UI data
    WEBSITE = os.getenv('WEBSITE')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')
    OWNER_ID = os.getenv('OWNER_ID')

    # DB data
    HOST = os.getenv('HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')


sensitive_data = SensitiveData
