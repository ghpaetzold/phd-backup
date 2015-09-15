import os

#Parameters:
ks = ['5', '6', '7']
Cs = ['1', '0.1', '0.01']
losses = ['hinge', 'squared_hinge']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for l in losses:
	for C in Cs:
		for k in ks:
			output = '../../labels/pa/labels_PAClassifier_'+l+'_'+C+'_'+k+'.txt'
			comm = 'nohup python Run_PAClassifier.py '+trainset+' '+k+' '+C+' '+l+' '+testset+' '+output+' &'
			os.system(comm)
