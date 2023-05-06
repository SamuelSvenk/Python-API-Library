from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v3/air-time/{book}")
async def air_time(book: str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT FIN.TICKET_NO,
                                FIN.PASSENGER_NAME,
                                ARRAY_AGG(ARRAY[FIN.ARRIVAL_AIRPORT::text,
                                    FIN.DEPARTURE_AIRPORT::text,
                                    TO_CHAR(FIN.FLIGHT_TIME, 'fmhh24:mi:ss'),
                                    TO_CHAR(FIN.TOTAL_TIME, 'fmhh24:mi:ss')])
                            FROM
                                (SELECT RF.FLIGHT_TIME,
                                        RF.PASSENGER_NAME,
                                        RF.PASSENGER_ID,
                                        RF.DEPARTURE_AIRPORT,
                                        RF.ARRIVAL_AIRPORT,
                                        RF.TICKET_NO,
                                        SUM(RF.ACTUAL_ARRIVAL - RF.ACTUAL_DEPARTURE) OVER (PARTITION BY RF.PASSENGER_ID	ORDER BY RF.ACTUAL_DEPARTURE) AS TOTAL_TIME
                                    FROM
                                        (SELECT FLIGHTS.ARRIVAL_AIRPORT,
                                                FLIGHTS.DEPARTURE_AIRPORT,
                                                FLIGHTS.ACTUAL_ARRIVAL,
                                                FLIGHTS.ACTUAL_DEPARTURE,
                                                (FLIGHTS.ACTUAL_ARRIVAL - FLIGHTS.ACTUAL_DEPARTURE) AS FLIGHT_TIME,
                                                TICKETS.BOOK_REF,
                                                TICKETS.TICKET_NO,
                                                TICKETS.PASSENGER_NAME,
                                                TICKETS.PASSENGER_ID
                                        
                                            FROM FLIGHTS
                                            JOIN BOARDING_PASSES ON (BOARDING_PASSES.FLIGHT_ID = FLIGHTS.FLIGHT_ID)
                                            JOIN TICKETS ON (TICKETS.TICKET_NO = BOARDING_PASSES.TICKET_NO)
                                            WHERE TICKETS.BOOK_REF = '{book}'
                                        ORDER BY TICKETS.TICKET_NO) AS RF
                                )AS FIN
                            GROUP BY FIN.PASSENGER_NAME, FIN.TICKET_NO """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []

    for row in rows:
        result = {} 
        result['ticket_no'] = row[0]
        result['passenger_name'] = row[1]
        result["flights"] = []

        for flight in row[2]:
            flights = {} 
            flights['arrival_airport'] = flight[0]
            flights['departure_airport'] = flight[1]
            flights['flight_time'] = flight[2]
            flights['total_time'] = flight[3]
            result['flights'].append(flights)

        endpoint.append(result)

    return {
        'results': endpoint
    }

    