from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
train_victor_corpus = sys.argv[2]
test_victor_corpus = sys.argv[3]
positive_range = int(sys.argv[4].strip())
folds = int(sys.argv[5].strip())
test_size = float(sys.argv[6].strip())
loss = sys.argv[7].strip()
penalty = sys.argv[8].strip()
alpha = float(sys.argv[9].strip())
l1_ratio = float(sys.argv[10].strip())
epsilon = float(sys.argv[11].strip())
features = sys.argv[12].strip()
if features!='all':
	features = int(features)
temp_file = sys.argv[13].strip()
out = sys.argv[14].strip()

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

br = BoundaryRanker(fe)

subs = getSubs(generator)

bs = BoundarySelector(br)

tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_train.txt')
bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
bs.trainSelectorWithCrossValidation(train_victor_corpus, positive_range, folds, test_size, k=features)

tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_test.txt')

#For each proportion, select and save:
proportions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
for proportion in proportions:
	bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
	selected = bs.selectCandidates(subs, test_victor_corpus, temp_file, proportion, proportion_type='integer')

	outf = open(out + '_' + str(proportion) + '.txt', 'w')
	vicf = open(test_victor_corpus)
	for cands in selected:
		data = vicf.readline().strip().split('\t')
		newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
		for cand in cands:
			newline += '0:'+cand + '\t'
		outf.write(newline.strip() + '\n')
	outf.close()
	vicf.close()
