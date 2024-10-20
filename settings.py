from decouple import config
import urllib.parse

DB_USER = config("DB_USER")
DB_PASSWORD = urllib.parse.quote_plus(config("DB_PASSWORD"))
DB_SERVER = config("DB_SERVER") 
DB_NAME = config("DB_NAME")

DATABASE_URL =f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"


