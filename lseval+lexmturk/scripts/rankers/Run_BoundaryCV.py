from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
folds = int(sys.argv[3].strip())
test_size = float(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()
k = sys.argv[7].strip()
if k!='all':
        k = int(k)

fe = FeatureEstimator()
fe.addLengthFeature('Complexity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Simplicity')

br = BoundaryRanker(fe)
br.trainRankerWithCrossValidation(victor_corpus, positive_range, folds, test_size)

ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
