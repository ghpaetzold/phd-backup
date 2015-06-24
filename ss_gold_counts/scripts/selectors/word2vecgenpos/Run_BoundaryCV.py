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
proportion = float(sys.argv[14].strip())
out = sys.argv[15].strip()

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

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'
fe = FeatureEstimator()
fe.addWordVectorSimilarityNormalFeature('/export/data/ghpaetzold/word2vecvectors/corpora/word_vectors_all.bin', 'Simplicity')
fe.addWordVectorSimilarityFeature('/export/data/ghpaetzold/word2vecvectors/corpora/word_vectors_all_generalized.bin', java, model, tagger, 'Simplicity')
fe.addCollocationalFeature('../../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
#fe.addCollocationalFeature('../../../../lexmturk/corpora/simplewiki.5.bin.txt', 2, 2, 'Complexity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/translation_probabilities_lexmturkall.txt', 'Simplicity')
condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'
#fe.addTargetPOSTagProbability(condprob_model, model, tagger, java, 'Simplicity')

br = BoundaryRanker(fe)

subs = getSubs(generator)

bs = BoundarySelector(br)
bs.trainSelectorWithCrossValidation(train_victor_corpus, positive_range, folds, test_size, k=features)
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
