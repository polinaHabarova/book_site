from fastapi import FastAPI
from app.routes.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")