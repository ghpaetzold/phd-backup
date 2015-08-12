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

def getTaggedSents(corpus):
        result = []
        f = open(corpus)
        for line in f:
                tags = []
                tokens = line.strip().split(' ')
                for token in tokens:
                        tokendata = token.strip().split('|||')
                        tags.append((tokendata[0].strip(), tokendata[1].strip()))
                result.append(tags)
        return result

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

condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')

br = SVMRanker(fe, '/export/tools/svm-rank')

subs = getSubs(generator)

bs = SVMRankSelector(br)
tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_train.txt')
bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
bs.trainSelector(train_victor_corpus, features_file, model_file, C, epsilon, kernel)

tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_test.txt')
bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
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
