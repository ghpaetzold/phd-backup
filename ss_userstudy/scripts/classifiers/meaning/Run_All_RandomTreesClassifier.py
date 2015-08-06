import os

#Parameters:
ks = ['all']
ns = ['25', '50']
cs = ['gini', 'entropy']
maxes = ['auto', 'sqrt', 'log2', 'None']

os.system('mkdir ../../../classes/meaning/randomtrees/')

trainset = '../../../datasets/meaning_victor_training.txt'
testset = '../../../datasets/meaning_victor_testing.txt'
for n in ns:
	for c in cs:
		for ma in maxes:
			for k in ks:
				output = '../../../classes/meaning/randomtrees/labels_RandomTreesClassifier_'+n+'_'+c+'_'+ma+'_'+k+'all.txt'
				comm = 'nohup python Run_RandomTreesClassifier.py '+trainset+' '+k+' '+n+' '+c+' '+ma+' '+testset+' '+output+' &'
				os.system(comm)
