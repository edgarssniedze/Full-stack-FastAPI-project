from fastapi import APIRouter, HTTPException, Depends, Form, Response
from fastapi.responses import RedirectResponse
from sqlmodel import select, or_, func

from app.database.db import SessionDep
from app.models.rental import Rental, RentalsPublic, RentalMovie
from app.models.movie import Movie
from uuid import UUID
from app.core.services import role_check, get_current_user
from datetime import datetime

rent = APIRouter(tags=["Rentals"], prefix="/api")

@rent.post("/rent/{movie_id}")
async def rent_movie(
    *,
    session: SessionDep,
    movie_id: UUID,
    user=Depends(get_current_user)
):

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
        response_description="Returns every rental and their details"
        )
async def get_rentals(*, session: SessionDep, user=Depends(get_current_user)):
    count = session.exec(
        select(func.count()).select_from(Rental)
    ).one()

    results = session.exec(
        select(Rental, Movie)
        .join(Movie, Rental.movie_id == Movie.id)
        .where(Rental.user_id == user.id)
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

@rent.post("/rent/return/{rental_id}")
async def return_movie(session: SessionDep, rental_id: UUID):
    rental = session.get(Rental, rental_id)

    if not rental:
        raise HTTPException(404, detail="Rental not found")
    
    rental.returned_at = datetime.now()

    session.delete(rental)
    session.commit()

    return RedirectResponse("/yourmovies", status_code=303)


def get_rented_movie_ids(session: SessionDep) -> set[UUID]:
    result = session.exec(
        select(Rental.movie_id)
        .where(Rental.returned_at == None)
    ).all()

    results = set(result)

    return results