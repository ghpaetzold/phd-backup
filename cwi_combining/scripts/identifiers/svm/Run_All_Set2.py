import os

#Parameters:
#ks = ['10', '50', '100', '200', 'all']
#ks = ['1', '2', '3']
ks = ['5', '6', 'all']
Cs = ['1', '0.1', '0.01']
Cs = ['1', '10']
kernels = ['rbf', 'poly', 'sigmoid']
kernels = ['rbf', 'sigmoid']
gammas = ['0.0', '1']

trainset = '../../../corpora/cwi_paetzold_training.txt'
testset = '../../../corpora/cwi_paetzold_testing.txt'
for C in Cs:
	for kernel in kernels:
		for g in gammas:
			for k in ks:
				output = '../../../labels/svm_set2/labels_SVMSet2_'+C+'_'+kernel+'_'+g+'_'+k+'.txt'
				comm = 'nohup python Run_Set2.py '+trainset+' '+k+' '+C+' '+kernel+' 3 '+g+' 0.0 '+testset+' '+output+' &'
				os.system(comm)
