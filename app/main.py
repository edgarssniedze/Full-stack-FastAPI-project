from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database.db import lifespan
from app.middleware.logger import response_log
from app.middleware.auth import AuthMiddleware

from .api.routes.auth import auth
from .api.routes.users import users 
from .api.routes.movies import movies
from  .views.views import views
from .api.routes.rent import rent
from .api.routes.password import reset

app = FastAPI(lifespan=lifespan)

app.include_router(auth)
app.include_router(users)
app.include_router(movies)
app.include_router(views)
app.include_router(rent)
app.include_router(reset)

app.middleware("http")(response_log)
app.add_middleware(AuthMiddleware)

@app.get("/",
         summary="root")
async def root():
    return RedirectResponse(url="/login", status_code=301)  
