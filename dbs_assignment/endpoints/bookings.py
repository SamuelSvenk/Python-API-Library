from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v1/bookings/{booking_id}")
async def bookings(booking_id: str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT  BOOKINGS.BOOK_REF,
                                BOOKINGS.BOOK_DATE,
                                TICKETS.TICKET_NO,
                                TICKETS.PASSENGER_ID,
                                TICKETS.PASSENGER_NAME,
                                BOARDING_PASSES.BOARDING_NO,
                                FLIGHTS.flight_no,
                                BOARDING_PASSES.SEAT_NO,
                                FLIGHTS.aircraft_code,
                                FLIGHTS.arrival_airport,
                                FLIGHTS.departure_airport,
                                FLIGHTS.scheduled_arrival,
                                FLIGHTS.scheduled_departure

                            FROM BOOKINGS
                            JOIN TICKETS ON (TICKETS.BOOK_REF = BOOKINGS.BOOK_REF)
                            JOIN TICKET_FLIGHTS ON(TICKET_FLIGHTS.TICKET_NO = TICKETS.TICKET_NO)
                            JOIN BOARDING_PASSES ON (BOARDING_PASSES.TICKET_NO = TICKET_FLIGHTS.TICKET_NO
                                                AND BOARDING_PASSES.FLIGHT_ID = TICKET_FLIGHTS.FLIGHT_ID)
                            JOIN FLIGHTS ON (FLIGHTS.FLIGHT_ID = TICKET_FLIGHTS.FLIGHT_ID)

                            WHERE BOOKINGS.BOOK_REF = '{booking_id}'
                            ORDER BY TICKETS.TICKET_NO,BOARDING_PASSES.BOARDING_NO
                                                                """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = {}
    endpoint['id'] = rows[0][0]
    endpoint['book_date'] = rows[0][1] 
    endpoint['boarding_passes'] = []

    for row in rows:
        boarding_passes = {}
        boarding_passes['id'] = row[2]
        boarding_passes['passenger_id'] = row[3]
        boarding_passes['passenger_name'] = row[4]
        boarding_passes['boarding_no'] = row[5]
        boarding_passes['flight_no'] = row[6]
        boarding_passes['seat'] = row[7]
        boarding_passes['aircraft_code'] = row[8]
        boarding_passes['arrival_airport'] = row[9]
        boarding_passes['departure_airport'] = row[10]
        boarding_passes['scheduled_arrival'] = row[11]
        boarding_passes['scheduled_departure'] = row[12]

        endpoint['boarding_passes'].append(boarding_passes)
        

    return {
        'result': endpoint
    }

    