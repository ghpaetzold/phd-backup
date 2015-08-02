import os
#1_0.005_0.00001
#Max file: ranks_modified_huber_l1_0.1_0.05_0.0001.txt

#lphas=[0.0001, 0.001, 0.01], l1_ratios=[0.0, 0.15, 0.25, 0.5, 0.75, 1.0]

#Parameters:
losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
losses = ['hinge', 'squared_hinge', 'modified_huber']
penalties = ['elasticnet']
alphas = ['0.0001', '0.001', '0.01']
l1ratios = ['0.0', '0.15', '0.25', '0.5', '0.75', '1.0']
epsilons = ['0.0001', '0.00001']

trainset = '../../corpora/semeval/semeval_train.txt'
testset = '../../corpora/semeval/semeval_test.txt'
for l in losses:
	for p in penalties:
		for a in alphas:
			for r in l1ratios:
				for e in epsilons:
					output = '../../rankings/paetzold/ranks_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'newcooc.txt'
					comm = 'nohup python Run_Paetzold.py '+trainset+' 1 '+l+' '+p+' '+a+' '+r+' '+e+' '+testset+' '+output+' &'
					os.system(comm)
