from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()

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

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_500_cbow.bin'

#Create feature estimator:
fe = FeatureEstimator(norm=False)
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 0, 0, 'Simplicity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 2, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 1, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 2, 2, 'Simplicity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
fe.addWordVectorSimilarityFeature(w2vmodel, 'Simplicity')
fe.addWordVectorContextSimilarityFeature(w2vmodel, model, tagger, java, 'Simplicity')

#Feature names:
featnames = []
featnames.append(r'WordLength')
featnames.append(r'NumberofSyllables')
featnames.append(r'FrequencySubIMDB')
featnames.append(r'FrequencySUBTLEX')
featnames.append(r'FrequencySimpleWiki')
featnames.append(r'FrequencyWikipedia')
featnames.append(r'FrequencyBrown')
featnames.append(r'SenseCount')
featnames.append(r'SynonymCount')
featnames.append(r'HypernymCount')
featnames.append(r'HyponymCount')
featnames.append(r'MinimumSenseDepth')
featnames.append(r'MaximumSenseDepth')
featnames.append(r'Ngramlef10right')
featnames.append(r'Ngramlef01right')
featnames.append(r'Ngramlef11right')
featnames.append(r'Ngramlef20right')
featnames.append(r'Ngramlef21right')
featnames.append(r'Ngramlef02right')
featnames.append(r'Ngramlef12right')
featnames.append(r'Ngramlef22right')
featnames.append(r'POSProb.')
featnames.append(r'TargetSim.')
featnames.append(r'ContextSim')

br = MetricRanker(fe)

for index in range(0, len(featnames)):
	method = featnames[index]

	tagged_sents = getTaggedSents('../../corpora/tagged_sents_NNSimpLex_test.txt')
	fe.temp_resources['tagged_sents'] = tagged_sents
	ranks = br.getRankings(test_victor_corpus, index)

	os.system('mkdir ../../rankings/'+method+'/')

	output_path = '../../rankings/'+method+'/ranks_'+method+'.txt'

	o = open(output_path, 'w')
	for rank in ranks:
		newline = ''
		for r in rank:
			newline += r + '\t'
		o.write(newline.strip() + '\n')
	o.close()
