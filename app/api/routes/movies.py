from fastapi import APIRouter, Depends, HTTPException, Response, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import select, col, func
from app.core.services import role_check
from app.models.movie import Movie, MovieCreate, MovieUpdate, MoviePublic, MoviesPublic
from app.database.db import SessionDep
from uuid import UUID
from datetime import datetime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
movies = APIRouter(tags=["Movies"], prefix="/api")

@movies.get(
        "/movies",
        summary="Lists all the movies",
        description="Lists all movies and their details",
        response_description="Returns every movie and their details",
        response_model=MoviesPublic
        )
async def get_movies(*, session: SessionDep):
    count = session.exec(
        select(func.count()).select_from(Movie)
    ).one()

    movies = session.exec(
        select(Movie).order_by(Movie.created.desc())
    ).all()

    return MoviesPublic(
        data=[MoviePublic.model_validate(m) for m in movies],
        count=count
    )    


@movies.post("/movie")
async def create_movie(
    *,
    session: SessionDep,
    title: str = Form(...),
    description: str = Form(...),
    year: int = Form(...),
    price: float = Form(...),
    role=Depends(role_check("admin"))
):
    dbmovie = Movie(
        title=title,
        description=description,
        year=year,
        price=price
    )

    session.add(dbmovie)
    session.commit()
    session.refresh(dbmovie)
    
    return RedirectResponse(url="/admin", status_code=301)


@movies.post("/update/{movie_id}",
              summary="Updates the movie details",
              description="Updates ALL values sent!",
              response_model=Movie,
              response_description="Updated movie information")
async def update_movie(
    session: SessionDep,
    movie_id: UUID,
    title: str = Form(None),
    description: str = Form(None),
    year: int = Form(None),
    price: float = Form(None),
    role=Depends(role_check("admin"))
    ):

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Item not found")

    if title is not None:
        movie.title = title
    if description is not None:
        movie.description = description
    if year is not None:
        movie.year = year
    if price is not None:
        movie.price = price

    movie.updated = datetime.now()

    session.commit()
    session.refresh(movie)

    return RedirectResponse("/admin", status_code=301)

@movies.get("/{movie_id}")
async def read_movie(
    request: Request,
    session: SessionDep,
    movie_id: UUID,
    role=Depends(role_check("admin"))
):
    movie = session.get(Movie, movie_id)

    if not movie:
        raise HTTPException(404, detail="Movie not found")

    return templates.TemplateResponse(
        request,
        "movie.html",{
            "request": request,
            "movie": movie,
        }
    )

@movies.post("/delete/{movie_id}",
              summary="Deletes a movie",
              description="Deletes a movie by id",
              response_description="Confirmation")
async def delete_movie(
    *, session: SessionDep, movie_id: UUID,
    role=Depends(role_check("admin"))
) -> Response:

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Movie not found")
    
    session.delete(movie)
    session.commit()
    
    return RedirectResponse("/admin", status_code=301)

