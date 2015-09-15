import os

#Parameters:
losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
losses = ['hinge', 'log', 'modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
alphas = ['0.001', '0.01', '0.1']
l1ratios = ['0.01', '0.05', '0.10', '0.15']
epsilons = ['0.0001', '0.001']

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/boundary')
for l in losses:
	for p in penalties:
		for a in alphas:
			for r in l1ratios:
				for e in epsilons:
					output = '../../sr_rankings/boundary/ranks_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'.txt'
					comm = 'nohup python Run_Boundary.py '+trainset+' 1 '+l+' '+p+' '+a+' '+r+' '+e+' '+testset+' '+output+' &'
					os.system(comm)
