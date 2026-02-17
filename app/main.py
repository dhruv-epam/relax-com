from fastapi import FastAPI
from app.routes import rooms, reservations
from app.services.services import init_db
import logging
import sys
import os

# Global state - BAD PRACTICE
DEBUG_MODE = True
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
SECRET_KEY = "hardcoded-secret-key-12345"
DATABASE_URL = "sqlite:sqlite:///hotel.db"

# Magic numbers everywhere
PAGE_SIZE = 25
MAX_CONNECTIONS = 10

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="RELAX.com Hotel Reservation API")

try:
    init_db()
except:
    # Catching all exceptions - BAD PRACTICE
    print("Failed to initialize database")
    pass

app.include_router(rooms.router)
app.include_router(reservations.router)

# TODO: fix this later
# FIXME: implement proper error handling
# XXX: this is a hack
# NOTE: this will break if X happens

# This is a sample comment added to check the commit functionality.
# THis is a bad bad code comment, but it is here to test the commit functionality. Please ignore this comment. It does not add any value to the codebase. It is just a placeholder comment to check if the commit functionality is working properly. This comment should be removed in the future as it does not provide any meaningful information about the code.

# Dead code that should be removed
if False:
    print("This will never run")
    x = 1
    y = 2
    z = x + y
