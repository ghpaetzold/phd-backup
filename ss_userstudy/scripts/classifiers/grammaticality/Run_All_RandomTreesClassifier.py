import os

generators = ['all']
#generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
#generators.remove('all')

#Parameters:
#ks = ['7', '10', 'all']
ks = ['all']
ns = ['25', '50']
cs = ['gini', 'entropy']
#maxes = ['auto', 'sqrt', 'log2', 'None']
maxes = ['auto']

for n in ns:
	for c in cs:
		for ma in maxes:
			for k in ks:
				for i in range(1, 6):
                                        for generator in generators:
                                                trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
                                                trainset += str(i) + '.txt'
                                                testset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/'
                                                testset += generator + '/substitutions_void.txt'
                                                output = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/' + generator + '/'
						output += 'substitutions_RandomTreesClassifierGrammaticality_'+n+'_'+c+'_'+ma+'_'+k+'_'+str(i)+'.txt'
						comm = 'nohup python Run_RandomTreesClassifier.py '+trainset+' '+k+' '+n+' '+c+' '+ma+' '+testset+' '+output+' &'
						os.system(comm)
