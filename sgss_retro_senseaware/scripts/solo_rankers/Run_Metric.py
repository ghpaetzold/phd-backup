from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
size = sys.argv[2].strip()
arch = sys.argv[3].strip()

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
mpath = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+size+'_'+arch+'.bin'
mpathR = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+size+'_'+arch+'_retrofitted.bin'
mpathSEM = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_'+size+'_'+arch+'.bin'
mpathRSEM = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_'+size+'_'+arch+'_retrofitted.bin'
condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addWordVectorSimilarityFeature(mpath, 'Simplicity')
fe.addWordVectorContextSimilarityFeature(mpath, model, tagger, java, 'Simplicity')
fe.addTaggedWordVectorSimilarityFeature(mpathSEM, model, tagger, java, 'paetzold', 'Simplicity')
fe.addTaggedWordVectorContextSimilarityFeature(mpathSEM, model, tagger, java, 'paetzold', 'Simplicity')
fe.addWordVectorSimilarityFeature(mpathR, 'Simplicity')
fe.addWordVectorContextSimilarityFeature(mpathR, model, tagger, java, 'Simplicity')
fe.addTaggedWordVectorSimilarityFeature(mpathRSEM, model, tagger, java, 'paetzold', 'Simplicity')
fe.addTaggedWordVectorContextSimilarityFeature(mpathRSEM, model, tagger, java, 'paetzold', 'Simplicity')

labelsmap = [('tgtsim', 'TEM'), ('cxtsim', 'TEM'), ('tgtsim', 'SEM'), ('cxtsim', 'SEM'), ('tgtsim', 'REM'), ('cxtsim', 'REM'), ('tgtsim', 'RSEM'), ('cxtsim', 'RSEM')]

br = MetricRanker(fe)

for index in range(0, 8):
	labels = labelsmap[index]
	method = labels[0]
	modeltype = labels[1]
	
	tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/tagged_sents_semeval_test.txt')
	fe.temp_resources['tagged_sents'] = tagged_sents
	ranks = br.getRankings(test_victor_corpus, index)

	os.system('mkdir ../../solo_rankings/'+method+'/')
	os.system('mkdir ../../solo_rankings/'+method+'/' + modeltype)
	os.system('mkdir ../../solo_rankings/'+method+'/' + modeltype + '/' + arch)
	os.system('mkdir ../../solo_rankings/'+method+'/' + modeltype + '/' + arch + '/' + size)

	output_path = '../../solo_rankings/'+method+'/'+modeltype+'/'+arch+'/'+size+'/ranks.txt'

	o = open(output_path, 'w')
	for rank in ranks:
		newline = ''
		for r in rank:
			newline += r + '\t'
		o.write(newline.strip() + '\n')
	o.close()
