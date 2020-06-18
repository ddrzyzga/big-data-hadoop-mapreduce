
import re

WORD_RE = re.compile(r'[\w]+')

words = WORD_RE.findall('Bid data, hadoop and map reduce. (hello world!)')
print(words)