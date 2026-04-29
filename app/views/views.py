from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.models.user import UserPublic
from app.api.routes.rent import get_rentals, get_rented_movie_ids
from app.core.services import get_current_user, role_check
from fastapi.templating import Jinja2Templates
from app.api.routes.movies import get_movies
from datetime import timedelta

views = APIRouter(tags=["Templates"])
templates = Jinja2Templates(directory="app/templates")
print(templates.env.loader)

@views.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request}
    )

@views.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html", 
        {"request": request}
    )

@views.get("/profile")
def profile_page(
    request: Request,
    curr_user: UserPublic | None = Depends(get_current_user)
):
    if not curr_user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error": "Not logged in"
            }
        )

    return templates.TemplateResponse(
        request,
        "profile.html",
        {
            "request": request,
            "user": curr_user
        }
    )

@views.get("/home")
def home(request: Request, movies=Depends(get_movies), rentals=Depends(get_rentals), rented_ids=Depends(get_rented_movie_ids)):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"request": request,
         "movies": movies,
         "rentals": rentals,
         "rented_ids": rented_ids}
    )

@views.get("/yourmovies")
def yourmovies(request: Request, curr_user: UserPublic = Depends(get_current_user), movies=Depends(get_movies), rentals=Depends(get_rentals)):
    return templates.TemplateResponse(
        request,
        "yourmovies.html",
        context={
            "request": request,
            "movies": movies,
            "rentals": rentals,
            "user": curr_user,
            "timedelta": timedelta
        }
    )

@views.get("/admin")
def admin_dash(
    request: Request,
    user=Depends(role_check("admin")),
    movies=Depends(get_movies),
):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request,
            "user": user,
            "movies": movies
        }
    ) 

