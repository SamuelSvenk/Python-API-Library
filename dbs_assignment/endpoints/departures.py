from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/departures")
async def departures(airport:str, day:int):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT FLIGHT_ID,
                            FLIGHT_NO,
                            SCHEDULED_DEPARTURE
                            
                        FROM FLIGHTS
                        WHERE DEPARTURE_AIRPORT = '{airport}' AND EXTRACT(ISODOW FROM SCHEDULED_DEPARTURE) = {day} AND status = 'Scheduled'
                        ORDER BY SCHEDULED_DEPARTURE ASC, FLIGHT_ID
                                                                    """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []
   
    for row in rows:
        result = {}
        result['flight_id'] = row[0]
        result['flight_no'] = row[1]
        result['scheduled_departure'] = row[2]

        endpoint.append(result)
        
    return {
        'results': endpoint
    }

    