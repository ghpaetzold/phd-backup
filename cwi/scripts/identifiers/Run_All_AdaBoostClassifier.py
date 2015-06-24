import os

#Parameters:
ks = ['5', '6', '7', '10']
ns = ['10', '25', '50']
lrs = ['0.1', '1', '10']
lrs = ['0.1']
algs = ['SAMME.R', 'SAMME']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for n in ns:
	for lr in lrs:
		for alg in algs:
			for k in ks:
				output = '../../labels/adaboost/labels_AdaBoostClassifier_'+n+'_'+lr+'_'+alg+'_'+k+'.txt'
				comm = 'nohup python Run_AdaBoostClassifier.py '+trainset+' '+k+' '+n+' '+lr+' '+alg+' '+testset+' '+output+' &'
				os.system(comm)
