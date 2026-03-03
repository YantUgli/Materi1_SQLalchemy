from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")


DATABASE_URL = F"mysql+pymysql://{username}:{password}@{host}:3306/{database}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    connection = engine.connect()
    print("Koneksi ke MariaDB Berhasil!")
    # connection.close()
except Exception as e:
    print(f"Gagal konek: {e}")