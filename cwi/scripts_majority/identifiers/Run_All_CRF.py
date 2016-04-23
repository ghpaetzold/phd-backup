import os

#Parameters:
learners = ['SubgradientSSVM', 'StructuredPerceptron', 'LatentSSVM', 'SubgradientLatentSSVM', 'PrimalDSStructuredSVM', 'FrankWolfeSSVM']
models = ['BinaryClf', 'GraphCRF', 'ChainCRF', 'GridCRF', 'MultiClassClf']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'

for learner in learners:
	for model in models:
		output = '../../labels/crf/labels_'+learner+'_'+model+'.txt'
		comm = 'nohup python Run_CRF.py '+trainset+' '+testset+' '+learner+' '+model+' '+output+' &'
		os.system(comm)
