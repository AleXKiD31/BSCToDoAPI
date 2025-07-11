from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL Format:
# mysql+pymysql://user:password@host:port/database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/todo_bsc"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
