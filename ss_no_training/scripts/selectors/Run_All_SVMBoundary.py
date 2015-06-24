import os

generators = os.listdir('../../substitutions/')
train_victor_corpus = '../../corpora/lexmturk_nosupervision.txt'
test_victor_corpus = '../../corpora/lexmturk_gold.txt'

#Parameters:
Cs = ['0.1', '1']
kernels = ['rbf', 'poly', 'linear', 'sigmoid']
degrees = ['2']
gammas = ['0.1', '1']
coef0s = ['0', '1']
proportions = ['1.0']

#Run Boundary selector:
c = 0
for generator in generators:
	for proportion in proportions:
		for C in Cs:
			for degree in degrees:
				for gamma in gammas:
					for coef0 in coef0s:
						c += 1
						temp_file = './temp/temp_file_svmboundary_' + str(c) + '.txt'
						out = '../../substitutions/'+generator+'/'
						out += 'substitutions_svmboundary_'+proportion+'_'+C+'_poly_'+degree+'_'+gamma+'_'+coef0+'.txt'
						comm = 'nohup python Run_SVMBoundary.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus
						comm += ' ' + temp_file + ' ' + C + ' poly ' + degree + ' ' + gamma + ' ' + coef0
						comm += ' ' + proportion + ' ' + out + ' &'
						os.system(comm)

for generator in generators:
	for proportion in proportions:
		for C in Cs:
			for gamma in gammas:
				c += 1
				temp_file = './temp/temp_file_svmboundary_' + str(c) + '.txt'
				out = '../../substitutions/'+generator+'/'
				out += 'substitutions_svmboundary_'+proportion+'_'+C+'_rbf_1_'+gamma+'_1.txt'
				comm = 'nohup python Run_SVMBoundary.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus
				comm += ' ' + temp_file + ' ' + C + ' rbf 1 ' + gamma + ' 1'
				comm += ' ' + proportion + ' ' + out + ' &'
				os.system(comm)
