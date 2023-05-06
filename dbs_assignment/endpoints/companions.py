from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/passengers/{passenger_id}/companions")
async def companions(passenger_id: str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" 
                        SELECT TICKETS.PASSENGER_ID,TICKETS.PASSENGER_NAME,
                            COUNT(TICKET_FLIGHTS.FLIGHT_ID) AS COUNT_FLIGHTS,
                            ARRAY_AGG(TICKET_FLIGHTS.FLIGHT_ID
                                        ORDER BY TICKET_FLIGHTS.FLIGHT_ID ASC)
                                        
                        FROM TICKET_FLIGHTS
                        JOIN TICKETS ON (TICKET_FLIGHTS.TICKET_NO = TICKETS.TICKET_NO)
                        WHERE TICKET_FLIGHTS.FLIGHT_ID IN
                                (SELECT TICKET_FLIGHTS.FLIGHT_ID
                                    FROM TICKET_FLIGHTS
                                    JOIN TICKETS ON (TICKET_FLIGHTS.TICKET_NO = TICKETS.TICKET_NO)
                                    WHERE TICKETS.PASSENGER_ID = '{passenger_id}')
                                            AND tickets.passenger_ID != '{passenger_id}'
                                            
                        GROUP BY TICKETS.PASSENGER_NAME,
                            TICKETS.PASSENGER_ID

                        ORDER BY COUNT_FLIGHTS DESC, TICKETS.PASSENGER_ID""")
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()


    endpoint = []

    for row in rows:
        results = {}
        results['id'] = row[0]
        results['name'] = row[1]
        results['flights_count'] = row[2]
        results['flights'] = row[3]

        endpoint.append(results)
        

    return {
        'results': endpoint
    }

    