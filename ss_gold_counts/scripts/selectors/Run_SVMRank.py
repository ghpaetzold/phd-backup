from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
train_victor_corpus = sys.argv[2]
test_victor_corpus = sys.argv[3]
C = float(sys.argv[4].strip())
kernel = int(sys.argv[5].strip())
epsilon = float(sys.argv[6].strip())
features_file = sys.argv[7].strip()
model_file = sys.argv[8].strip()
temp_file = sys.argv[9].strip()
te_features_file = sys.argv[10].strip()
scores_file = sys.argv[11].strip()
proportion = float(sys.argv[12].strip())
out = sys.argv[13].strip()

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

br = SVMRanker(fe, '/export/tools/svm-rank')

subs = getSubs(generator)

bs = SVMRankSelector(br)
bs.trainSelector(train_victor_corpus, features_file, model_file, C, epsilon, kernel)
selected = bs.selectCandidates(subs, test_victor_corpus, te_features_file, scores_file, temp_file, proportion)

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
