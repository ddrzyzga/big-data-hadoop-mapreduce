from mrjob.job import MRJob
from mrjob.step import MRStep

class MRFlights(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        year, items = line.split('\t')
        year=year[1:-1]
        items = items[1:-1]
        month, day, airline, distance =items.split(', ')
        distance = int(distance)
        yield None, distance

    def reducer(self, key, values):
        total = 0
        num_elements = 0

        for value in values:
            total += value
            num_elements +=1

        yield None,  total/num_elements

if __name__ == '__main__':
    MRFlights.run()