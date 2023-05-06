from fastapi import APIRouter

from dbs_assignment.connect import con

router = APIRouter()


@router.get("/v3/aircrafts/{aircraftcode}/top-incomes")
async def top_incomes(aircraftcode: str):

    connect = con()

    cursor = connect.cursor()
    cursor.execute(f""" SELECT xd.total_amount::int, to_char(to_date(xd.months, 'YYYY-MM'), 'YYYY-FMMM'), xd.days_int::text
                        FROM(SELECT x.days_int, x.months, MAX(x.total_amount) OVER (PARTITION BY x.months),x.total_amount
                            FROM(SELECT SUM(d.amount) AS total_amount, d.days, TO_CHAR(d.days::date, 'YYYY-MM') as months, EXTRACT(DAY FROM d.days::date) AS days_int
                                FROM(SELECT FLIGHTS.ACTUAL_DEPARTURE, TICKET_FLIGHTS.amount, TO_CHAR(ACTUAL_DEPARTURE, 'YYYY-MM-DD') as days
                                    FROM FLIGHTS
                                    JOIN TICKET_FLIGHTS ON (TICKET_FLIGHTS.FLIGHT_ID = FLIGHTS.FLIGHT_ID)
                                    WHERE FLIGHTS.actual_departure IS NOT NULL AND FLIGHTS.AIRCRAFT_CODE = '{aircraftcode}'
                                    ) AS d
                                GROUP BY d.days
                                )AS x
                            )AS xd

                        WHERE xd.total_amount = xd.max
                        ORDER BY xd.total_amount DESC, xd.months """)
    
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    endpoint = []

    for row in rows:
        result = {} 
        result['total_amount'] = row[0]
        result['month'] = row[1]
        result['day'] = row[2]
        
        endpoint.append(result)

    return {
        'results': endpoint
    }

    