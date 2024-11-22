import os

from sqlalchemy import create_engine
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)
