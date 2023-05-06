from fastapi import FastAPI

from dbs_assignment.router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DBS")
app.include_router(router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)