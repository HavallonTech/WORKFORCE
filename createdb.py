import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute(
    f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"
)

print("Database verified.")

conn.close()