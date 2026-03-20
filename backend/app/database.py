import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f'mysql+mysqlconnector://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)
