from fastapi import APIRouter
from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/airlines/{flight_no}/load-week")
async def load_week(flight_no:str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT OK.DAYS, ROUND(AVG(OK.percentage_load)::numeric,2)
                        FROM (
                            SELECT ((LK.load::float / AR.aircraft_capacity::float) * 100) AS percentage_load,
                                to_char(SCHEDULED_DEPARTURE, 'ID') AS DOW,
                                    to_char(SCHEDULED_DEPARTURE, 'Day') AS Days
                                    
                        FROM FLIGHTS
                        JOIN AIRCRAFTS_DATA ON (AIRCRAFTS_DATA.aircraft_code = flights.aircraft_code)  
                        JOIN (
                                SELECT COUNT(ticket_flights.ticket_no) AS "load", flights.flight_id
                                FROM FLIGHTS
                                JOIN TICKET_FLIGHTS ON (TICKET_FLIGHTS.FLIGHT_ID = FLIGHTS.FLIGHT_ID)
                                GROUP BY flights.flight_id
                            ) AS LK ON LK.flight_id = flights.flight_id      

                        JOIN (
                                SELECT COUNT(SEATS.SEAT_NO) AS "aircraft_capacity", aircraft_code
                                FROM SEATS
                                GROUP BY aircraft_code
                            ) AS AR ON AR.aircraft_code = AIRCRAFTS_DATA.aircraft_code

                        WHERE flights.flight_no = '{flight_no}'
                        GROUP BY flights.flight_id, DOW, AR.aircraft_capacity, LK.load,Days
                            ) AS OK

                        GROUP BY OK.DAYS, OK.DOW
                        ORDER BY OK.DOW ASC
                                                """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    result = {}
    result['flight_no'] = flight_no
    result['monday'] = rows[0][1]
    result['tuesday'] = rows[1][1]
    result['wednesday'] = rows[2][1]
    result['thursday'] = rows[3][1]
    result['friday'] = rows[4][1]
    result['saturday'] = rows[5][1]
    result['sunday'] = rows[6][1]
        
        
    return {
        'result': result
    }

    