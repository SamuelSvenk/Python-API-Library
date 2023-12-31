from fastapi import APIRouter
from dbs_assignment.endpoints import users,cards,authors,categories,publications, instances, rentals, reservations

router = APIRouter()

router.include_router(users.router, tags=["users"])
router.include_router(cards.router, tags=["cards"])
router.include_router(authors.router, tags=["authors"])
router.include_router(categories.router, tags=["categories"])
router.include_router(publications.router, tags=["publications"])
router.include_router(instances.router, tags=["instances"])
router.include_router(rentals.router, tags=["rentals"])
router.include_router(reservations.router, tags=["reservations"])
