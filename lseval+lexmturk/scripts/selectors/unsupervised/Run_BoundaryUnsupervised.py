from lexenstein.selectors import *
from lexenstein.rankers import *
from lexenstein.features import *
import sys

generator = sys.argv[1]
train_victor_corpus = sys.argv[2]
positive_range = int(sys.argv[3].strip())
loss = sys.argv[4].strip()
penalty = sys.argv[5].strip()
alpha = float(sys.argv[6].strip())
l1_ratio = float(sys.argv[7].strip())
epsilon = float(sys.argv[8].strip())
temp_file = sys.argv[9].strip()
proportion = float(sys.argv[10].strip())
out = sys.argv[11].strip()
test_victor_corpus = sys.argv[12].strip()

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
	f = open('../../../substitutions/' + generator + '/substitutions.txt')
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
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 2, 'Simplicity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')

br = BoundaryRanker(fe)

subs = getSubs(generator)

bs = BoundarySelector(br)
tagged_sents = None

tagged_sents = getTaggedSents('../../../corpora/tagged_sents_paetzold_nns_dataset.txt')
bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
bs.trainSelector(train_victor_corpus, positive_range, loss, penalty, alpha, l1_ratio, epsilon)

tagged_sents = getTaggedSents('../../../corpora/tagged_sents_paetzold_nns_dataset.txt')
bs.ranker.fe.temp_resources['tagged_sents'] = tagged_sents
selected = bs.selectCandidates(subs, test_victor_corpus, temp_file, proportion, proportion_type='percentage')

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
