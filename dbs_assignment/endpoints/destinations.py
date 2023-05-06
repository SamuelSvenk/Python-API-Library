from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/airports/{airport}/destinations")
async def destinations(airport:str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT DISTINCT arrival_airport
                        FROM FLIGHTS
                        WHERE departure_airport = '{airport}'
                        ORDER BY arrival_airport ASC
                                                        """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []
   
    for row in rows:
        
        endpoint.append(row[0])
        
    return {
        'results': endpoint
    }

    