from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
folds = int(sys.argv[3].strip())
test_size = float(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()
type = sys.argv[7].strip()
size = sys.argv[8].strip()
arch = sys.argv[9].strip()

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
        f.close()
        return result

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
#fe.addCollocationalFeature('/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
if 'S' in type:
        fe.addTaggedWordVectorSimilarityFeature(mpath, model, tagger, java, 'paetzold', 'Simplicity')
	fe.addTaggedWordVectorContextSimilarityFeature(mpath, model, tagger, java, 'paetzold', 'Simplicity')
else:
        fe.addWordVectorSimilarityFeature(mpath, 'Simplicity')
	fe.addWordVectorContextSimilarityFeature(mpath, model, tagger, java, 'Simplicity')

br = BoundaryRanker(fe)

tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/tagged_sents_semeval_train.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
br.trainRankerWithCrossValidation(victor_corpus, positive_range, folds, test_size, k=8)

tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/tagged_sents_semeval_test.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
