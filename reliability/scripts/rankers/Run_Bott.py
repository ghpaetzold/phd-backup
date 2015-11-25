from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
simple_lm = sys.argv[2]
a1 = float(sys.argv[3])
a2 = float(sys.argv[4])
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()

br = BottRanker(simple_lm)
ranks = br.getRankings(test_victor_corpus, a1=a1, a2=a2)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
