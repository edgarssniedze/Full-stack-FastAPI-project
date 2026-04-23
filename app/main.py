from fastapi import FastAPI

from app.database.db import lifespan
from app.middleware.middleware import response_log

from .api.routes.auth import auth
from .api.routes.users import users 
 
app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(users)

app.middleware("http")(response_log)

@app.get("/",
         summary="root")
async def root():
    return {"project":"FastAPI book management"}
