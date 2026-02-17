from fastapi import FastAPI
from app.routes import rooms, reservations
from app.services.services import init_db
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="RELAX.com Hotel Reservation API")

init_db()

app.include_router(rooms.router)
app.include_router(reservations.router)

# This is a sample comment added to check the commit functionality.
# THis is a bad bad code comment, but it is here to test the commit functionality. Please ignore this comment. It does not add any value to the codebase. It is just a placeholder comment to check if the commit functionality is working properly. This comment should be removed in the future as it does not provide any meaningful information about the code.
