from lexenstein.rankers import *
from lexenstein.features import *
import sys

test_victor_corpus = sys.argv[1].strip()
output_path = sys.argv[2].strip()

fe = FeatureEstimator()
fe.addCollocationalFeature('../../../machinelearningranking/corpora/lm/subtleximdb.5gram.unk.bin.txt', 0, 0, 'Complexity')

br = MetricRanker(fe)

ranks = br.getRankings(test_victor_corpus, 0)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
