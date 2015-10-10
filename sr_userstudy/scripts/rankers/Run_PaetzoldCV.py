from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
folds = int(sys.argv[3].strip())
test_size = float(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
#fe.addCollocationalFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
#fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 0, 0, 'Complexity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
#fe.addSentenceProbabilityFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 'Complexity')
#fe.addSentenceProbabilityFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
#fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_1300_cbow_retrofitted.bin'
posw2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_1300_cbow_retrofitted.bin'
#fe.addTaggedWordVectorContextSimilarityFeature(posw2vmodel, model, tagger, java, 'paetzold', 'Simplicity')
fe.addWordVectorSimilarityFeature(w2vmodel, 'Simplicity')
fe.addWordVectorContextSimilarityFeature(w2vmodel, model, tagger, java, 'Simplicity')

br = BoundaryRanker(fe)
br.trainRankerWithCrossValidation(victor_corpus, positive_range, folds, test_size)

ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
