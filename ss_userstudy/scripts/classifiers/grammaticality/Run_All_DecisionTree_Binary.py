import os

#Generators:
generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
generators.remove('all')

#Parameters:
ks = ['all']
#ks = ['all']
criterions = ['gini', 'entropy']
#criterions = ['gini']
splitters = ['best']
maxes = ['sqrt']
depths = ['4', 'None']
#depths = ['None']

for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					for i in range(1, 6):
						for generator in generators:
							trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
							trainset += str(i) + '.txt'
							testset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/'
							testset += generator + '/substitutions_void.txt'
							output = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/' + generator + '/'
							output += 'substitutions_DecisionTreeBinGrammaticality_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'_'+str(i)+'_allfeats.txt'
							comm = 'nohup python Run_DecisionTree_Binary.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
							os.system(comm)
