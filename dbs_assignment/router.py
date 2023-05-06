from fastapi import APIRouter
from dbs_assignment.endpoints import companions,bookings,late_departure,top_airlines,departures,destinations,load,load_week,seat_choice,air_time,top_incomes,users,cards, authors


router = APIRouter()
router.include_router(companions.router, tags=["companions"])
router.include_router(bookings.router, tags=["bookings"])
router.include_router(late_departure.router, tags=["late_departure"])
router.include_router(top_airlines.router, tags=["top_airlines"])
router.include_router(departures.router, tags=["departures"])
router.include_router(destinations.router, tags=["destinations"])
router.include_router(load.router, tags=["load"])
router.include_router(load_week.router, tags=["load_week"])
router.include_router(seat_choice.router, tags=["seat_choice"])
router.include_router(air_time.router, tags=["air_time"])
router.include_router(top_incomes.router, tags=["top_incomes"])
router.include_router(users.router, tags=["users"])
router.include_router(cards.router, tags=["cards"])
router.include_router(authors.router, tags=["authors"])
