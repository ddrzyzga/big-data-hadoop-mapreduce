from mrjob.job import MRJob
from mrjob.step import MRStep

class MRFlight(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer_init=self.reducer_init,
                   reducer=self.reducer)
        ]
    def configure_args(self):
        super(MRFlight, self).configure_args()
        self.add_file_arg('--airlines', help='Path to the airlines.csv')

    def mapper(self, _, line):
        (year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport,
         destination_airport, scheduled_departure, departure_time, departure_delay, taxi_out,
         wheels_off, scheduled_time, elapsed_time, air_time, distance, wheels_on, taxi_in,
         scheduled_arrival, arrival_time, arrival_delay, diverted, cancelled, cancellation_reason,
         air_system_delay, security_delay, airline_delay, late_aircraft_delay, weather_delay) = line.split(',')

        if departure_delay=='':
            departure_delay=0
        if arrival_delay=='':
            arrival_delay=0

        departure_delay=float(departure_delay)

        arrival_delay=float(arrival_delay)

        yield airline, (departure_delay, arrival_delay)

    def reducer_init(self):
        self.airline_names = {}

        with open('airlines.csv', 'r') as file:
            for line in file:
                code, full_name = line.split(',')
                full_name = full_name[:-1]
                self.airline_names[code] = full_name #dla klucza code zwroc mi full_name

    def reducer(self, key, values):
        total_dep_delay=0
        total_arr_delay=0
        num_elem=0

        for value in values:
            total_dep_delay +=value[0]
            total_arr_delay +=value[1]
            num_elem +=1
        yield self.airline_names[key], (total_dep_delay/num_elem, total_arr_delay/num_elem)

if __name__ == '__main__':
    MRFlight.run()