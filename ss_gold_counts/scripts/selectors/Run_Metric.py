from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
out = sys.argv[3].strip()

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

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 0, 2, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 1, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 2, 'Simplicity')
fe.addNGramProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Simplicity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/transprob_dict_lexmturk.bin', 'Simplicity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')

br = MetricRanker(fe)
tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_test.txt')
br.fe.temp_resources['tagged_sents'] = tagged_sents
selected = br.getRankings(test_victor_corpus, index)

outf = open(out, 'w')
vicf = open(test_victor_corpus)
for cands in selected:
        data = vicf.readline().strip().split('\t')
	ocands = data[3:len(data)]
        newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
        for cand in cands:
                newline += '0:'+cand + '\t'
        outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
