import os

#Parameters:
ks = ['4', '5', '6', '7', 'all']
ks = ['all']
Cs = ['1', '0.1', '2']
#Cs = ['1', '10']
kernels = ['rbf', 'sigmoid']
#kernels = ['sigmoid']
gammas = ['0.0', '1', '10']

trainset = '../../corpora/cwi_paetzold_training'
testset = '../../corpora/cwi_paetzold_testing'
for C in Cs:
	for kernel in kernels:
		for g in gammas:
			for k in ks:
				output = '../../labels/shardlow/labels_Shardlow_'+C+'_'+kernel+'_'+g+'_'+k
				comm = 'nohup python Run_Shardlow.py '+trainset+' '+k+' '+C+' '+kernel+' 3 '+g+' 0.0 '+testset+' '+output+' &'
				os.system(comm)
