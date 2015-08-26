import os

#Parameters:
Cs = ['1']
kernels = ['3']
epsilons = ['0.00001']

generators = os.listdir('../../substitutions/')

train_victor_corpus = '../../corpora/lexmturk_gold_train.txt'
test_victor_corpus = '../../corpora/lexmturk_gold_test.txt'

#Run SVMRank selector:
c = 0
for generator in generators:
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
				out += 'substitutions_svmranknotgt1st_'+C+'_'+k+'_'+e
				comm = 'nohup python Run_SVMRank.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' ' + C + ' '
				comm += k + ' ' + e + ' ' + features_file + ' ' + model_file + ' ' + temp_file + ' '
				comm += te_features_file + ' ' + scores_file + ' ' + out + ' &'
				os.system(comm)
