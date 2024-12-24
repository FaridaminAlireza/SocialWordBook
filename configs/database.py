import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database engine (SQLite for this example)
SQL_LITE_DB_URL = "sqlite:///example_1.db"

env_path = find_dotenv()
load_dotenv(env_path)

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

DB_NAME = os.getenv("DB_NAME", "dictionary")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session(arg):
    db = SessionLocal()

    try:

        def decorator(func):
            def wrapper(*args, **kwargs):
                print(*args)
                print(**kwargs)
                kwargs["db"] = db
                result = func(*args, **kwargs)  # Call the original function
                return result

            return wrapper

        return decorator
    finally:
        db.close()


def create_all_tables():
    # Create all tables in the engine
    Base.metadata.create_all(bind=engine)
