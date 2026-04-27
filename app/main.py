from fastapi import FastAPI

from app.database.db import lifespan
from app.middleware.middleware import response_log

from .api.routes.auth import auth
from .api.routes.users import users 
from .api.routes.movies import movies
from  .views.views import views

app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(users)
app.include_router(movies)
app.include_router(views)

app.middleware("http")(response_log)

@app.get("/",
         summary="root")
async def root():
    return {"project":"FastAPI book management"}
