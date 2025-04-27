from fastapi import FastAPI
from fastapi.security import HTTPBearer
from database.database import Base, engine
from routers.routers import router


app = FastAPI()
app.include_router(router)
http_bearer = HTTPBearer()

Base.metadata.create_all(bind=engine)
