from fastapi import APIRouter, Request, Depends
from app.models.user import UserPublic
from app.core.security import get_current_user
from fastapi.templating import Jinja2Templates

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