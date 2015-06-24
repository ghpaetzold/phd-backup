import os

#Parameters:
Cs = ['1', '0.1']
#Cs = ['1']
kernels = ['0', '1', '3']
#kernels = ['1']
epsilons = ['0.0001']
proportions = ['0.125', '0.25', '0.5']

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_gold_targetfirst.txt'

#Run SVMRank selector:
c = 0
for generator in generators:
	for proportion in proportions:
		for C in Cs:
			for k in kernels:
				for e in epsilons:
					c += 1
					temp_file = './temp/temp_file_svmrank_' + str(c) + '.txt'
					features_file = './temp/features_file_svmrank_' + str(c) + '.txt'
					model_file = './temp/model_file_svmrank_' + str(c) + '.txt'
					te_features_file = './temp/te_features_file_svmrank_' + str(c) + '.txt'
					scores_file = './temp/scores_file_svmrank_' + str(c) + '.txt'
					out = '../../substitutions/'+generator+'/'
					out += 'substitutions_svmrank_'+proportion+'_'+C+'_'+k+'_'+e+'.txt'
					comm = 'nohup python Run_SVMRank.py ' + generator + ' ' + victor_corpus + ' ' + C + ' '
					comm += k + ' ' + e + ' ' + features_file + ' ' + model_file + ' ' + temp_file + ' '
					comm += te_features_file + ' ' + scores_file + ' ' + proportion + ' ' + out + ' &'
					os.system(comm)
