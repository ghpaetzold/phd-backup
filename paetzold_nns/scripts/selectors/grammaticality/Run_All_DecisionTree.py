import os

#Generators:
generators = os.listdir('../..//substitutions/')
#generators.remove('all')

#Parameters:
ks = ['all']
criterions = ['gini', 'entropy']
splitters = ['best']
maxes = ['sqrt']
depths = ['4', 'None']

for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					for i in range(1, 6):
						for generator in generators:
							trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
							trainset += str(i) + '.txt'
							testset = '../../substitutions/'
							testset += generator + '/substitutions_void.txt'
							output = '../../substitutions/' + generator + '/'
							output += 'substitutions_GrammaticalityDT_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'_'+str(i)+'_allfeats.txt'
							comm = 'nohup python Run_Grammaticality.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
							os.system(comm)
