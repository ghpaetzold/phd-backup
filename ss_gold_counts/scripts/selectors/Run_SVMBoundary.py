from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
train_victor_corpus = sys.argv[2]
test_victor_corpus = sys.argv[3]
temp_file = sys.argv[4].strip()
C = float(sys.argv[5].strip())
kernel = sys.argv[6].strip()
degree = int(sys.argv[7].strip())
gamma = float(sys.argv[8].strip())
coef0 = float(sys.argv[9].strip())
proportion = float(sys.argv[10].strip())
out = sys.argv[11].strip()

def getSubs(generator):
	result = {}
	f = open('../../substitutions/' + generator + '/substitutions.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		candidates = data[1].strip().split('|||')
		result[target] = candidates
	f.close()
	return result

fe = FeatureEstimator()
fe.addWordVectorSimilarityFeature('../../../lexmturk/corpora/word_vectors_all.bin', 'Simplicity')
fe.addCollocationalFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addCollocationalFeature('../../../lexmturk/corpora/simplewiki.5.bin.txt', 2, 2, 'Complexity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/translation_probabilities_lexmturkall.txt', 'Simplicity')

br = SVMBoundaryRanker(fe)

subs = getSubs(generator)

bs = SVMBoundarySelector(br)
bs.trainSelector(train_victor_corpus, 1, C, kernel, degree, gamma, coef0)
selected = bs.selectCandidates(subs, test_victor_corpus, temp_file, proportion)

outf = open(out, 'w')
vicf = open(test_victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
