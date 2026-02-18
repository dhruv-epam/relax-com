from fastapi import FastAPI
from app.routes import rooms, reservations
from app.services.services import init_db
import logging
import sys
import os
import pickle  # Unused import - security risk
import subprocess  # Unused import - security risk

# Global state - BAD PRACTICE
DEBUG_MODE = True
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
SECRET_KEY = "hardcoded-secret-key-12345"
DATABASE_URL = "sqlite:sqlite:///hotel.db"
ADMIN_PASSWORD = "admin123"  # Hardcoded credentials
API_KEY = "sk-1234567890abcdef"  # Exposed API key
AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"  # AWS credentials in code

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

# Dangerous eval usage
def execute_user_input(user_input: str):
    """Execute arbitrary code from user input - VERY DANGEROUS!"""
    result = eval(user_input)  # Security vulnerability: arbitrary code execution
    return result

# Using exec for dynamic code - security risk
def run_dynamic_code(code: str):
    exec(code)  # Another security vulnerability

# Password stored in plain text
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "qwerty",
    "test": "test123"
}

# Insecure random for security-sensitive operations
import random
def generate_token():
    return str(random.randint(100000, 999999))  # Should use secrets module
