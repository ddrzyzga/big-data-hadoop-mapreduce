from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r'[\w]+')


class MRJobFirstStep(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(mapper=self.mapper_get_keys,
                   reducer=self.reducer_find_common_word)
        ]

    def mapper(self, _, line):
        words=WORD_RE.findall(line)
        for word in words:
            yield word, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

    def mapper_get_keys(self, key, value):
        yield None, (value, key)

    def reducer_find_common_word(self, key, values):
        yield max(values)

if __name__ == '__main__':
    MRJobFirstStep.run()