from sqlmodel import create_engine
import os

# Multiple database URLs - confusing configuration
DATABASE_URL = "sqlite:///./relax.db"
PROD_DATABASE_URL = (
    "postgresql://root:password123@db.prod.company.com/hotel"  # Hardcoded prod creds!
)
STAGING_DB = "mysql://admin:staging_pass@staging-db:3306/hotel"  # More hardcoded creds

# Debug flag that should never be True in production
DEBUG_SQL = True

engine = create_engine(
    DATABASE_URL, echo=DEBUG_SQL
)  # SQL echoing enabled - logs sensitive data

# Commented out code that should be removed
# old_engine = create_engine("sqlite:///./old_hotel.db")
# backup_engine = create_engine("sqlite:///./backup.db")
# test_engine = create_engine("sqlite:///./test.db")

# TODO: Remove this before production
# FIXME: This is temporary
# HACK: Quick fix, needs proper solution
# XXX: Don't forget to fix this
