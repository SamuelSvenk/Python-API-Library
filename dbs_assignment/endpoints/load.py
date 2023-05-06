from decimal import *
from fastapi import APIRouter
from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/airlines/{flight_no}/load")
async def load(flight_no:str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT flights.flight_id, AR.aircraft_capacity, LK.load,
                        ROUND(((LK.load::float / AR.aircraft_capacity::float) * 100)::numeric,2) AS percentage_load
                        FROM FLIGHTS
                        JOIN AIRCRAFTS_DATA ON (AIRCRAFTS_DATA.aircraft_code = flights.aircraft_code)  
                        JOIN (SELECT COUNT(ticket_flights.ticket_no) AS "load",
                                    flights.flight_id
                                    FROM FLIGHTS
                                    JOIN TICKET_FLIGHTS ON (TICKET_FLIGHTS.FLIGHT_ID = FLIGHTS.FLIGHT_ID)
                                    GROUP BY FLIGHTS.FLIGHT_ID) AS LK ON LK.flight_id = flights.flight_id
                                    
                        JOIN (SELECT COUNT(SEATS.SEAT_NO) AS "aircraft_capacity",	seats.aircraft_code
                            FROM SEATS
                            GROUP BY seats.aircraft_code) AS AR ON AR.aircraft_code = AIRCRAFTS_DATA.aircraft_code
                        WHERE FLIGHTS.flight_no = '{flight_no}'
                                                        """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []
   
    for row in rows:
        result = {}
        result['id'] = row[0]
        result['aircraft_capacity'] = row[1]
        result['load'] = row[2]
        result['percentage_load'] = Decimal(row[3]).normalize()

        endpoint.append(result)
        
    return {
        'results': endpoint
    }

    