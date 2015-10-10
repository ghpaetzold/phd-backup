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

fe = FeatureEstimator()
fe.addCollocationalFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 0, 0, 'Complexity')
#fe.addCollocationalFeature('../../../machinelearningranking/corpora/lm/subtlex.5gram.bin.txt', 2, 2, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 'Complexity')
fe.addSentenceProbabilityFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
#fe.addSentenceProbabilityFeature('../../../machinelearningranking/corpora/lm/subtlex.5gram.bin.txt', 'Complexity')
fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')


br = SVMRanker(fe, '/export/data/ghpaetzold/modifiedsvmrank/scripts/versions/top3/')
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
