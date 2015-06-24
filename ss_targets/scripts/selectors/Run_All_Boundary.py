import os

#Parameters:
losses = ['hinge', 'modified_huber']
penalties = ['elasticnet']
alphas = ['0.001', '0.01', '0.1']
#alphas = ['0.1']
l1ratios = ['0.0', '0.15', '0.25', '0.5', '0.75', '1.0']
#l1ratios = ['0.1']
epsilons = ['0.0001', '0.00001']
#epsilons = ['0.0001']
proportions = ['1.0']

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_gold.txt'

#Run Boundary selector:
c = 0
for generator in generators:
	for proportion in proportions:
		for l in losses:
			for p in penalties:
				for a in alphas:
					for r in l1ratios:
						for e in epsilons:
							c += 1
							temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
							out = '../../substitutions/'+generator+'/'
							out += 'substitutions_boundary_'+proportion+'_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'.txt'
							comm = 'nohup python Run_Boundary.py ' + generator + ' ' + victor_corpus + ' 1 ' + l + ' '
							comm += p + ' ' + a + ' ' + r + ' ' + e + ' ' + temp_file + ' ' + proportion + ' ' + out + ' 0 &'
							os.system(comm)
