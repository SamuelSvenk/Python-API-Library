from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v3/aircrafts/{aircraftcode}/seats/{rank}")
async def seatchoice(aircraftcode: str, rank: int):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT RF.SEAT_NO, COUNT(RF.SEAT_NO)
                        FROM
                            (SELECT FLIGHTS.FLIGHT_ID,
                                    FLIGHTS.AIRCRAFT_CODE,
                                    BOARDING_PASSES.SEAT_NO,
                                    DENSE_RANK() OVER (PARTITION BY FLIGHTS.FLIGHT_ID ORDER BY BOOKINGS.BOOK_DATE) AS RANK
                                FROM BOOKINGS
                                JOIN TICKETS ON (TICKETS.BOOK_REF = BOOKINGS.BOOK_REF)
                                JOIN BOARDING_PASSES ON (BOARDING_PASSES.TICKET_NO = TICKETS.TICKET_NO)
                                JOIN FLIGHTS ON (FLIGHTS.FLIGHT_ID = BOARDING_PASSES.FLIGHT_ID)
                                WHERE FLIGHTS.AIRCRAFT_CODE = '{aircraftcode}') AS RF
                                
                        WHERE RF.RANK = {rank} 
                        GROUP BY RF.SEAT_NO
                        ORDER BY COUNT DESC
                        LIMIT 1""")
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = {}
   
    endpoint['seat'] = rows[0][0]
    endpoint['count'] = rows[0][1]

   
    return {
        'result': endpoint
    }

    