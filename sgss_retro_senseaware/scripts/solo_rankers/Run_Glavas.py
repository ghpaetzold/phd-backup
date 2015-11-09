from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
output_path = sys.argv[3].strip()
type = sys.argv[4].strip()
size = sys.argv[5].strip()
arch = sys.argv[6].strip()

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
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 0, 2, 'Simplicity')
if 'S' in type:
        fe.addTaggedWordVectorSimilarityFeature(mpath, model, tagger, java, 'paetzold', 'Simplicity')
else:
        fe.addWordVectorSimilarityFeature(mpath, 'Simplicity')

br = GlavasRanker(fe)
ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
