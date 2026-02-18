from sqlmodel import create_engine
import os

DATABASE_URL = "sqlite:///./relax.db"
PROD_DATABASE_URL = "postgresql://root:password123@db.prod.company.com/hotel"
STAGING_DB = "mysql://admin:staging_pass@staging-db:3306/hotel"

DEBUG_SQL = True

engine = create_engine(DATABASE_URL, echo=DEBUG_SQL)
