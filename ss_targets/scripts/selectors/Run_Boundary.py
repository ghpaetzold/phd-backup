from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
positive_range = int(sys.argv[3].strip())
loss = sys.argv[4].strip()
penalty = sys.argv[5].strip()
alpha = float(sys.argv[6].strip())
l1_ratio = float(sys.argv[7].strip())
epsilon = float(sys.argv[8].strip())
temp_file = sys.argv[9].strip()
proportion = float(sys.argv[10].strip())
out = sys.argv[11].strip()
doCV = sys.argv[12].strip()

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
#fe.addCollocationalFeature('../../corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addCollocationalFeature('../../../lexmturk/corpora/simplewiki.5.bin.txt', 2, 2, 'Complexity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/translation_probabilities_lexmturkall.txt', 'Simplicity')

br = BoundaryRanker(fe)

subs = getSubs(generator)

bs = BoundarySelector(br)
if doCV!='1':
	bs.trainSelector(victor_corpus, positive_range, loss, penalty, alpha, l1_ratio, epsilon)
else:
	bs.trainSelectorWithCrossValidation(victor_corpus, positive_range, 5, 0.25)
selected = bs.selectCandidates(subs, victor_corpus, temp_file, proportion)

outf = open(out, 'w')
vicf = open(victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t' + '0:'+data[1] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
