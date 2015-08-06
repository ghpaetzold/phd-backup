import os

generators = ['all']
#generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
#generators.remove('all')

#Parameters:
#ks = ['4', '5', '6', '7', 'all']
ks = ['all']
#Cs = ['1', '0.1', '0.01']
Cs = ['1.0', '0.1']
kernels = ['rbf', 'linear', 'sigmoid']
#kernels = ['rbf']
gammas = ['0.0', '1.0']

for C in Cs:
	for kernel in kernels:
		for g in gammas:
			for k in ks:
				for i in range(1, 6):
					for generator in generators:
						trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
						trainset += str(i) + '.txt'
						testset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/'
						testset += generator + '/substitutions_void.txt'
						output = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/' + generator + '/'
						output += 'substitutions_SVMClassifierGrammaticality_'+C+'_'+kernel+'_'+g+'_'+k+'_'+str(i)+'.txt'
						comm = 'nohup python Run_SVM.py '+trainset+' '+k+' '+C+' '+kernel+' 2 '+g+' 0.0 '+testset+' '+output+' &'
						os.system(comm)
