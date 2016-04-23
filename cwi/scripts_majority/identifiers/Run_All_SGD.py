import os

#Parameters:
#losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
ks = ['6', '7', '8']
losses = ['hinge', 'squared_hinge', 'modified_huber']
#losses = ['modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
#penalties = ['l2']
alphas = ['0.001', '0.01', '0.1']
alphas = ['0.1']
l1ratios = ['0.05', '0.10', '0.15']
l1ratios = ['0.15']
epsilons = ['0.0001', '0.01', '0.1']
epsilons = ['0.1']

trainset = '../../corpora/cwi_paetzold_training_conservative.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for l in losses:
	for p in penalties:
		for a in alphas:
			for r in l1ratios:
				for e in epsilons:
					for k in ks:
						output = '../../labels_majority/sgd/labels_SGDClassifier_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'_'+k+'.txt'
						comm = 'nohup python Run_SGDClassifier.py '+trainset+' '+k+' '+l+' '+p+' '+a+' '+r+' '+e+' '+testset+' '+output+' &'
						os.system(comm)
