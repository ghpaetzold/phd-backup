from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
train_feature_file = sys.argv[2]
c = float(sys.argv[3].strip())
epsilon = float(sys.argv[4].strip())
kernel = int(sys.argv[5].strip())
model_file = sys.argv[6].strip()
test_feature_file = sys.argv[7].strip()
scores_file = sys.argv[8].strip()
test_victor_corpus = sys.argv[9].strip()
output_path = sys.argv[10].strip()
type = sys.argv[11].strip()
size = sys.argv[12].strip()
arch = sys.argv[13].strip()

#Open model:
mpath = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if 'S' in type:
        mpath += 'generalized_'
mpath += size + '_' + arch
if 'R' in type:
        mpath += '_retrofitted'
mpath += '.bin'

condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/transprob_dict_lexmturk.bin', 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 0, 'Simplicity')
fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 'Simplicity')
fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt', 'Simplicity')
fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 2, 2, 'Simplicity')

br = SVMRanker(fe, '/export/tools/svm-rank/')
br.getFeaturesFile(victor_corpus, train_feature_file)
br.getTrainingModel(train_feature_file, c, epsilon, kernel, model_file)
br.getFeaturesFile(test_victor_corpus, test_feature_file)
br.getScoresFile(test_feature_file, model_file, scores_file)

ranks = br.getRankings(test_feature_file, scores_file)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
