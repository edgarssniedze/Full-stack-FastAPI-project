from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select, col, func
from app.core.security import get_current_user
from app.models.movie import Movie, MovieCreate, MovieUpdate, MoviePublic, MoviesPublic
from app.database.db import SessionDep
from uuid import UUID

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

@movies.post(
        "/movie",
        summary="Creates a movie",
        description="Creates a movie with provided details",
        response_description="Information about the movie",
        response_model= Movie)
async def create_movie(
    *, session: SessionDep, movie_in: MovieCreate
) -> Movie:
    dbmovie = Movie.model_validate(movie_in)
    session.add(dbmovie)
    session.commit()
    session.refresh(dbmovie)
    return dbmovie

@movies.patch("/{movie_id}",
              summary="Updates the movie details",
              description="Updates ALL values sent!",
              response_model=Movie,
              response_description="Updated movie information")
async def update_movie(
    *, session: SessionDep, movie_in: MovieUpdate, movie_id: UUID
) -> Movie:

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Item not found")

    update = movie_in.model_dump(exclude_unset=True)

    for field, value in update.items():
        setattr(movie, field, value)

    session.commit()
    session.refresh(movie)

    return movie

@movies.get("/{movie_id}",
              summary="Reads the movie details",
              description="Returns all details of a movie",
              response_model=Movie,
              response_description="Details of a movie")
async def read_movie(
    *, session: SessionDep, movie_id: UUID
) -> Movie:

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Movie not found")

    return movie

@movies.delete("/{movie_id}",
              summary="Deletes a movie",
              description="Deletes a movie by id",
              response_description="Confirmation")
async def delete_movie(
    *, session: SessionDep, movie_id: UUID
) -> Response:

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Movie not found")
    
    session.delete(movie)
    session.commit()
    
    return Response(status_code=204)