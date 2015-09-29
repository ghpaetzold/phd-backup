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

#Generators:
generators = ['all']
generators = ['paetzold']

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
fe.addCandidatePOSNominalFeature(model, tagger, java, pos_type='treebank')
#fe.addCandidatePOSNominalFeature(model, tagger, java, pos_type='paetzold')
fe.addPOSNgramNominalFeature(0, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramNominalFeature(1, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramNominalFeature(1, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramNominalFeature(0, 2, model, tagger, java, pos_type='treebank')
fe.addPOSNgramNominalFeature(2, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramNominalFeature(2, 2, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramNominalFeature(1, 1, model, tagger, java, pos_type='paetzold')
fe.addPOSNgramWithCandidateNominalFeature(0, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(1, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(1, 1, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(0, 2, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(2, 0, model, tagger, java, pos_type='treebank')
fe.addPOSNgramWithCandidateNominalFeature(2, 2, model, tagger, java, pos_type='treebank')
#fe.addPOSNgramWithCandidateNominalFeature(1, 1, model, tagger, java, pos_type='paetzold')

for generator in generators:
	#Calculate features:
	print('Getting features...')
	tagged_sents = getTaggedSents('../../../../corpora/tagged_sents_ls_dataset_benchmarking.txt')
	fe.temp_resources['tagged_sents'] = tagged_sents
	features = fe.calculateFeatures('../../../../substitutions/'+generator+'/substitutions_void.txt', format='victor')

	#Produce temp file:
	print('Creating temp file...')
	o = open('../../../../corpora/wcefiles/temp/'+generator+'.txt', 'w')
	f = open('../../../../substitutions/'+generator+'/substitutions_void.txt')
	c = -1
	for line in f:
		data = line.strip().split('\t')
		for cand in data[3:]:
			c += 1
			values = features[c]
			newline = '1\t'
			for value in values:
				newline += str(value) + '\t'
			o.write(newline.strip() + '\n')
	f.close()
	o.close()

	#Get models available:
	algs = os.listdir('../../../../corpora/wcefiles/models/')
	for alg in algs:
		models = os.listdir('../../../../corpora/wcefiles/models/'+alg+'/')
		for model in models:
			prefix = model[0:len(model)-4]
			comm = '/export/tools/crfsuite/bin/crfsuite tag -m '
			comm += '../../../../corpora/wcefiles/models/'+alg+'/'+model+' '
			comm += '../../../../corpora/wcefiles/temp/'+generator+'.txt > '
			comm += '../../../../corpora/wcefiles/temp/labels_'+generator+'_'+alg+'_'+prefix+'.txt'
			os.system(comm)
			
			f = open('../../../../corpora/wcefiles/temp/labels_'+generator+'_'+alg+'_'+prefix+'.txt')
			lex = open('../../../../substitutions/'+generator+'/substitutions_void.txt')
			o = open('../../../../substitutions/'+generator+'/substitutions_crfunsupervised_'+alg+'_'+prefix+'.txt', 'w')
			for line in lex:
				data = line.strip().split('\t')
				newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
				for cand in data[3:]:
					label = f.readline().strip()
					if label=='1':
						newline += cand + '\t'
				o.write(newline.strip() + '\n')
			f.close()
			lex.close()
			o.close()
