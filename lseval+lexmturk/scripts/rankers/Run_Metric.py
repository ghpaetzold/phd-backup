from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
output_path = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 0, 0, 'Simplicity')
br = MetricRanker(fe)

ranks = br.getRankings(test_victor_corpus, index)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
