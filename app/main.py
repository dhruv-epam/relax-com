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
