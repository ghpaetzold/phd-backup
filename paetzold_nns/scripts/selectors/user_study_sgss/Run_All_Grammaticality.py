import os

#Generators:
generators = os.listdir('../../../substitutions/')
#generators.remove('all')

#Parameters:
ks = ['all']
criterions = ['gini']
splitters = ['best']
maxes = ['sqrt']
depths = ['None']

for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					for generator in generators:
						trainset = '/export/data/ghpaetzold/user_study_sgss/datasets/grammaticality_victor_all_optimistic.txt'
						testset = '../../../substitutions/'
						testset += generator + '/substitutions_void.txt'
						output = '../../../substitutions/' + generator + '/'
						output += 'substitutions_GrammaticalityUS_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'.txt'
						comm = 'nohup python Run_Grammaticality.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
						os.system(comm)
