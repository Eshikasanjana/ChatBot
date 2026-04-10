import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

root_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=root_path)
Database_url=os.getenv("URL_DATABASE")
if not Database_url:
    raise ValueError("URL_DATABASE not found in .env file!")

engine = create_engine(Database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()