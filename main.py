from fastapi import (FastAPI)

from app.routers import capture, subscribe
from app.utils.manager import ConnectionManager

manager = ConnectionManager()
app = FastAPI()

app.include_router(subscribe.router)
app.include_router(capture.router)