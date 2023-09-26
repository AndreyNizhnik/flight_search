class FlightDataOneWay:

    def __init__(self, count, price, origin_city, origin_airport,
                 destination_city, destination_airport,
                 out_date, out_time,
                 arrive_date, arrive_time, duration, stopovers_count):
        self.count = count
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.out_time = out_time
        self.arrive_date = arrive_date
        self.arrive_time = arrive_time
        self.duration = duration
        self.stopovers_count = stopovers_count


class FlightDataRound(FlightDataOneWay):

    def __init__(self, count, price, origin_city, origin_airport,
                 destination_city, destination_airport,
                 out_date, out_time,
                 arrive_date, arrive_time, duration, stopovers_count,
                 back_out_date, back_out_time, back_arrive_date, back_arrive_time,
                 back_stopovers_count, back_duration
                 ):
        super().__init__(count, price, origin_city, origin_airport,
                         destination_city, destination_airport,
                         out_date, out_time,
                         arrive_date, arrive_time, duration, stopovers_count)
        self.back_out_date = back_out_date
        self.back_out_time = back_out_time
        self.back_arrive_date = back_arrive_date
        self.back_arrive_time = back_arrive_time
        self.back_stopovers_count = back_stopovers_count
        self.back_duration = back_duration
