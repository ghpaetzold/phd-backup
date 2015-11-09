import os

#Parameters:
losses = ['hinge', 'modified_huber']
penalties = ['elasticnet']
alphas = ['0.001', '0.01', '0.1']
#alphas = ['0.1']
l1ratios = ['0.15', '0.25', '0.5', '0.75']
#l1ratios = ['0.1']
epsilons = ['0.00001']
#epsilons = ['0.0001']
proportions = ['0.25', '0.5', '0.75']

generators = os.listdir('../../substitutions/')
generators = ['paetzold']

#train_victor_corpus = '../../corpora/lexmturk_all_targetfirst.txt'
#train_victor_corpus = '../../corpora/lexmturk_all.txt'
train_victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

test_victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

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
							comm = 'nohup python Run_Boundary.py ' + generator + ' ' + train_victor_corpus + ' 1 ' + l + ' '
							comm += p + ' ' + a + ' ' + r + ' ' + e + ' ' + temp_file + ' ' + proportion + ' ' + out + ' '
							comm += test_victor_corpus +' &'
							os.system(comm)
