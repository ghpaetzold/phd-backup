from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
loss = sys.argv[3].strip()
penalty = sys.argv[4].strip()
alpha = float(sys.argv[5].strip())
l1_ratio = float(sys.argv[6].strip())
epsilon = float(sys.argv[7].strip())
test_victor_corpus = sys.argv[8].strip()
output_path = sys.argv[9].strip()

fe = FeatureEstimator()
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')

br = BoundaryRanker(fe)
br.trainRanker(victor_corpus, positive_range, loss, penalty, alpha, l1_ratio, epsilon)

ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
