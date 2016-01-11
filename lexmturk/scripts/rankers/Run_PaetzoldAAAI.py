from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
output_path = sys.argv[2].strip()

fe = FeatureEstimator()
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')

br = MetricRanker(fe)
print('estimated for: ' + output_path)

ranks = br.getRankings(test_victor_corpus, 0)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
