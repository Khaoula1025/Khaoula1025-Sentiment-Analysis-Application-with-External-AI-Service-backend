from sqlalchemy.orm import declarative_base , sessionmaker
from sqlalchemy import create_engine 




DATABASE_URL = 'sqlite:///./users.db'
Base = declarative_base()
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()