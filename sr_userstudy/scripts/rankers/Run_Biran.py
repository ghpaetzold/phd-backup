from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
simple_lm = sys.argv[2]
complex_lm = sys.argv[3]
test_victor_corpus = sys.argv[4].strip()
output_path = sys.argv[5].strip()

br = BiranRanker(complex_lm, simple_lm)
ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
