from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
positive_range = int(sys.argv[3].strip())
folds = int(sys.argv[4].strip())
test_size = float(sys.argv[5].strip())
temp_file = sys.argv[6].strip()
proportion = float(sys.argv[7].strip())
out = sys.argv[8].strip()

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
bs.trainSelectorWithCrossValidation(victor_corpus, positive_range, folds, test_size)
selected = bs.selectCandidates(subs, victor_corpus, temp_file, proportion)

outf = open(out, 'w')
vicf = open(victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
