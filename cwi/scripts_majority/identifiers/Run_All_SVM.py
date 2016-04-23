import os

#Parameters:
ks = ['4', '5', '6', '7', 'all']
#ks = ['1', '2', '3']
Cs = ['1', '0.1', '0.01']
Cs = ['0.01', '0.1']
kernels = ['rbf', 'poly', 'sigmoid']
kernels = ['rbf']
gammas = ['0.0', '1']

trainset = '../../corpora/cwi_paetzold_training_conservative.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for C in Cs:
	for kernel in kernels:
		for g in gammas:
			for k in ks:
				output = '../../labels_majority/svm/labels_SVMClassifier_'+C+'_'+kernel+'_'+g+'_'+k+'.txt'
				comm = 'nohup python Run_SVM.py '+trainset+' '+k+' '+C+' '+kernel+' 3 '+g+' 0.0 '+testset+' '+output+' &'
				os.system(comm)
