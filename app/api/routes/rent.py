from fastapi import APIRouter, HTTPException, Depends, Form, Response
from fastapi.responses import RedirectResponse
from sqlmodel import select, or_, func

from app.database.db import SessionDep
from app.models.rental import Rental, RentalsPublic, RentalMovie
from app.models.movie import Movie
from uuid import UUID
from app.core.services import role_check
from datetime import datetime

rent = APIRouter(tags=["Rentals"], prefix="/api")

@rent.post("/rent/{movie_id}")
async def rent_movie(
    *,
    session: SessionDep,
    movie_id: UUID,
    role=Depends(role_check("admin"))
):
    user = role

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404, detail="Movie not found")

    rental = Rental(
        user_id=user.id,
        movie_id=movie.id,
        cost=movie.price,
        rented_at=datetime.now()
    )

    session.add(rental)
    session.commit()
    session.refresh(rental)

    return RedirectResponse("/yourmovies", status_code=303)

@rent.get(
        "/rentals",
        summary="Lists all the rentals",
        description="Lists all rentals and their details",
        response_description="Returns every rental and their details",
        )
async def get_rentals(*, session: SessionDep):
    count = session.exec(
        select(func.count()).select_from(Rental)
    ).one()

    results = session.exec(
        select(Rental, Movie)
        .join(Movie, Rental.movie_id == Movie.id)
        .order_by(Rental.created.desc())
    ).all()

    return RentalsPublic(
    data=[
        RentalMovie(
            rental=r,
            movie=m
        )
        for r, m in results
    ],
    count=count
)