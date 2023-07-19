import databases
import sqlalchemy
from decouple import config

DATABASE_URL = config("DB_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
