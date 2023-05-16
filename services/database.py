import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

database_url = f"mysql+pymysql://{os.getenv('PS_USERNAME')}:{os.getenv('PS_PASSWORD')}@{os.getenv('PS_HOST')}/{os.getenv('PS_DATABASE')}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = get_db()
