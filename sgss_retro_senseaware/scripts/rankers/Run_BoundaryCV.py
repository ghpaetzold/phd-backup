from lexenstein.rankers import *
from lexenstein.features import *
import sys

for i in range(1, 10):
	print(str(i) + ': ' + sys.argv[i])
victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
folds = int(sys.argv[3].strip())
test_size = float(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()
type = sys.argv[7].strip()
size = sys.argv[8].strip()
arch = sys.argv[9].strip()

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
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
if 'S' in type:
        fe.addTaggedWordVectorSimilarityFeature(mpath, model, tagger, java, 'paetzold', 'Simplicity')
else:
        fe.addWordVectorSimilarityFeature(mpath, 'Simplicity')

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
