import os

#Parameters:
ks = ['7', '10', 'all']
ns = ['25', '50']
lrs = ['1', '10']
losses = ['deviance', 'exponential']
maxes = ['auto', 'sqrt', 'log2', 'None']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/ls_dataset_benchmarking.txt'
os.system('mkdir ../../labels/gradientboost/')
for n in ns:
	for lr in lrs:
		for loss in losses:
			for ma in maxes:
				for k in ks:
					output = '../../labels/gradientboost/labels_GradientBoostClassifier_'+n+'_'+lr+'_'+loss+'_'+ma+'_'+k+'.txt'
					comm = 'nohup python Run_GradientBoostClassifier.py '+trainset+' '+k+' '+n+' '+lr+' '+loss+' '+ma+' '+testset+' '+output+' &'
					os.system(comm)
