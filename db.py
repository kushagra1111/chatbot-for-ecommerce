
from sqlalchemy import create_engine  # Import create_engine to connect to DB
from models import Base  # Import Base from models

engine = create_engine("sqlite:///./test.db")  # Create SQLite engine (change URL for PostgreSQL/MySQL)
Base.metadata.create_all(bind=engine)  # Create all tables
