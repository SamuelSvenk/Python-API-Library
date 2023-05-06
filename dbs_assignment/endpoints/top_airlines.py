from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/top-airlines")
async def limit(limit: int):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT FLIGHTS.FLIGHT_NO,
                            COUNT(TICKET_FLIGHTS.TICKET_NO) AS "count"
                        FROM FLIGHTS
                        JOIN TICKET_FLIGHTS ON (TICKET_FLIGHTS.FLIGHT_ID = FLIGHTS.FLIGHT_ID)
                        WHERE flights.status = 'Arrived'
                        GROUP BY FLIGHTS.FLIGHT_NO
                        ORDER BY "count" DESC, FLIGHTS.FLIGHT_NO
                        LIMIT {limit}
                                """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []
   
    for row in rows:
        result = {}
        result['flight_no'] = row[0]
        result['count'] = row[1]

        endpoint.append(result)
        
    return {
        'results': endpoint
    }

    