from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables using the exact keys from your .env
USER = os.getenv("SUPABASE_USERNAME")
PASSWORD = os.getenv("SUPABASE_PASSWORD")
HOST = os.getenv("SUPABASE_HOST")
PORT = os.getenv("SUPABASE_PORT")
DBNAME = os.getenv("SUPABASE_DBNAME")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Initialize MetaData and reflect the existing Supabase schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Map the reflected tables to variables for easy access in your routes
users_table = metadata.tables.get('users')
meetings_table = metadata.tables.get('meetings')
payments_table = metadata.tables.get('payments')

# Create a configured "SessionLocal" class for generating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session in FastAPI routes safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the connection and reflection
try:
    with engine.connect() as connection:
        print("Connection and schema reflection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")