from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
C = float(sys.argv[3].strip())
kernel = int(sys.argv[4].strip())
epsilon = float(sys.argv[5].strip())
features_file = sys.argv[6].strip()
model_file = sys.argv[7].strip()
temp_file = sys.argv[8].strip()
te_features_file = sys.argv[9].strip()
scores_file = sys.argv[10].strip()
proportion = float(sys.argv[11].strip())
out = sys.argv[12].strip()

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
fe.addWordVectorSimilarityFeature('/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_500_cbow.bin', 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
#fe.addCollocationalFeature('../../corpora/simplewiki.5.bin.txt', 2, 2, 'Complexity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/transprob_dict_lexmturk.bin', 'Simplicity')

br = SVMRanker(fe, '/export/tools/svm-rank')

subs = getSubs(generator)

bs = SVMRankSelector(br)
bs.trainSelector(victor_corpus, features_file, model_file, C, epsilon, kernel)
selected = bs.selectCandidates(subs, victor_corpus, te_features_file, scores_file, temp_file, proportion)

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
