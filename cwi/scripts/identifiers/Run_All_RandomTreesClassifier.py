import os

#Parameters:
ks = ['7', '10', 'all']
ns = ['25', '50']
cs = ['gini', 'entropy']
maxes = ['auto', 'sqrt', 'log2', 'None']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for n in ns:
	for c in cs:
		for ma in maxes:
			for k in ks:
				output = '../../labels/randomtrees/labels_RandomTreesClassifier_'+n+'_'+c+'_'+ma+'_'+k+'.txt'
				comm = 'nohup python Run_RandomTreesClassifier.py '+trainset+' '+k+' '+n+' '+c+' '+ma+' '+testset+' '+output+' &'
				os.system(comm)
