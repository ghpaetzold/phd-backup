from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
simple_lm = sys.argv[2]
cooc_model = sys.argv[3]
a1 = float(sys.argv[4])
a2 = float(sys.argv[5])
a3 = float(sys.argv[6])
a4 = float(sys.argv[7])
a5 = float(sys.argv[8])
test_victor_corpus = sys.argv[9].strip()
output_path = sys.argv[10].strip()

br = YamamotoRanker(simple_lm, cooc_model)
ranks = br.getRankings(test_victor_corpus, a1=a1, a2=a2, a3=a3, a4=a4, a5=a5)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
