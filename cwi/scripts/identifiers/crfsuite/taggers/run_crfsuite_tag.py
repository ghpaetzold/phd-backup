import os
from lexenstein.features import *

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
ngram_file = '/export/data/ghpaetzold/LEXenstein/corpora/ngram_dict_wmt_simplewiki_1billion_webbase.bin'

fe = FeatureEstimator(norm=False)
fe.addBackoffBehaviorNominalFeature(ngram_file, 'Simplicity')
fe.addCandidateNominalFeature()
fe.addNgramNominalFeature(0, 1)
fe.addNgramNominalFeature(1, 0)
fe.addNgramNominalFeature(1, 1)
fe.addNgramNominalFeature(0, 2)
fe.addNgramNominalFeature(2, 0)
fe.addNgramNominalFeature(2, 2)
#fe.addCandidatePOSNominalFeature(model, tagger, java, pos_type='treebank')
fe.addCandidatePOSNominalFeature(model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(0, 1, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(1, 0, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(1, 1, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(0, 2, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(2, 0, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(2, 2, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(1, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(0, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(1, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(1, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(0, 2, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(2, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(2, 2, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramWithCandidateNominalFeature(1, 1, model, tagger, java, pos_type='treebank')

#Calculate features:
print('Getting features...')
tagged_sents = getTaggedSents('../../../../corpora/tagged_sents_testing.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
features = fe.calculateFeatures('../../../../corpora/cwi_paetzold_testing.txt', format='cwictor')

#Produce temp file:
print('Creating temp file...')
o = open('../datasets/testing.txt', 'w')
f = open('../../../../corpora/cwi_paetzold_testing.txt')
c = -1
for line in f:
	c += 1
	data = line.strip().split('\t')
	values = features[c]
	label = data[3].strip()
	newline = label + '\t'
	for value in values:
		newline += str(value) + '\t'	
	o.write(newline.strip() + '\n')
f.close()
o.close()

#Get models available:
algs = os.listdir('../models/')
for alg in algs:
	models = os.listdir('../models/'+alg+'/')
	for model in models:
		prefix = model[0:len(model)-4]
		comm = '/export/tools/crfsuite/bin/crfsuite tag -m '
		comm += '../models/'+alg+'/'+model+' '
		comm += '../datasets/testing.txt > '
		comm += '../../../../labels/crfsuite/labels_CRFSuite_'+alg+'_'+prefix+'.txt'
		os.system(comm)
