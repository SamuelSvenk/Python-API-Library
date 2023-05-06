from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/flights/late-departure/{delay}")
async def delay(delay: int):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT FLIGHT_ID,
                                FLIGHT_NO,
                                EXTRACT(EPOCH FROM(ACTUAL_DEPARTURE - SCHEDULED_DEPARTURE) / 60)::INT AS DELAY
                        FROM FLIGHTS
                        WHERE EXTRACT(EPOCH FROM(ACTUAL_DEPARTURE - SCHEDULED_DEPARTURE) / 60)::INT IS NOT NULL
                                AND EXTRACT(EPOCH FROM(ACTUAL_DEPARTURE - SCHEDULED_DEPARTURE) / 60)::INT >= {delay}
                        ORDER BY DELAY DESC,
                                FLIGHT_ID ASC
                                                """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []
   
    for row in rows:
        result = {}
        result['flight_id'] = row[0]
        result['flight_no'] = row[1]
        result['delay'] = row[2]

        endpoint.append(result)
        
    return {
        'results': endpoint
    }

    