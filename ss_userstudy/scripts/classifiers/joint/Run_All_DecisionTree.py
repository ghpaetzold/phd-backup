import os

#Generators:
generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
generators = ['all']

#Parameters:
ks = ['all']
criterions = ['gini', 'entropy']
splitters = ['best']
maxes = ['sqrt']
depths = ['None']

for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					for i in range(1, 6):
						for generator in generators:
							trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_meaning_victor_training_'
							trainset += str(i) + '.txt'
							testset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/'
							testset += generator + '/substitutions_void.txt'
							output = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/' + generator + '/'
							output += 'substitutions_DecisionTreeJoint_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'_'+str(i)+'_all.txt'
							comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset
							comm += ' '+output+' &'
							#print(comm)
							os.system(comm)
