from fastapi import APIRouter
import psycopg2

from dbs_assignment.config import settings

def con():
    connect = psycopg2.connect(host = settings.DATABASE_HOST,
                        port = settings.DATABASE_PORT,
                        database = settings.DATABASE_NAME,
                        user = settings.DATABASE_USER,
                        password = settings.DATABASE_PASSWORD,
                        options="-c search_path=bookings")
    return connect


