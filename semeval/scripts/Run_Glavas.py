from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
output_path = sys.argv[3].strip()

fe = FeatureEstimator()
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')

br = GlavasRanker(fe)
ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
