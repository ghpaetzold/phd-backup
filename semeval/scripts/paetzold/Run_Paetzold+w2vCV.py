from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
positive_range = int(sys.argv[2].strip())
folds = int(sys.argv[3].strip())
test_size = float(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
output_path = sys.argv[6].strip()

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

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')

br = BoundaryRanker(fe)
tagged_sents = getTaggedSents('../../corpora/semeval/tagged_sents_semeval_train.txt')
br.fe.temp_resources['tagged_sents'] = tagged_sents
br.trainRankerWithCrossValidation(victor_corpus, positive_range, folds, test_size)

tagged_sents = getTaggedSents('../../corpora/semeval/tagged_sents_semeval_test.txt')
br.fe.temp_resources['tagged_sents'] = tagged_sents
ranks = br.getRankings(test_victor_corpus)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
