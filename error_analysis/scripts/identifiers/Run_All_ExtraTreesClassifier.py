import os

#Parameters:
ks = ['7', '10', 'all']
ns = ['25', '50']
cs = ['gini', 'entropy']
classes = ['auto', 'subsample']
maxes = ['auto', 'sqrt', 'log2', 'None']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/ls_dataset_benchmarking.txt'
os.system('mkdir ../../labels/extratrees/')
for n in ns:
	for c in cs:
		for clas in classes:
			for ma in maxes:
				for k in ks:
					output = '../../labels/extratrees/labels_ExtraTreesClassifier_'+n+'_'+c+'_'+clas+'_'+ma+'_'+k+'.txt'
					comm = 'nohup python Run_ExtraTreesClassifier.py '+trainset+' '+k+' '+n+' '+c+' '+clas+' '+ma+' '+testset+' '+output+' &'
					os.system(comm)
