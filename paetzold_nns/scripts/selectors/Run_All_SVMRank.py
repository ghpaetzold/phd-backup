import os

#Parameters:
Cs = ['1']
kernels = ['0', '2', '3']
#kernels = ['1']
epsilons = ['0.0001']
proportions = ['7', '14']

generators = os.listdir('../../substitutions/')
generators = ['all', 'biran', 'glavas', 'kauchak']
generators = ['merriam', 'yamamoto']

train_victor_corpus = '../../corpora/lexmturk_all.txt'
test_victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

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
					out += 'substitutions_svmrank_'+proportion+'_'+C+'_'+k+'_'+e+'posprob.txt'
					comm = 'nohup python Run_SVMRank.py ' + generator + ' ' + train_victor_corpus + ' ' + C + ' '
					comm += k + ' ' + e + ' ' + features_file + ' ' + model_file + ' ' + temp_file + ' '
					comm += te_features_file + ' ' + scores_file + ' ' + proportion + ' ' + out + ' ' + test_victor_corpus + ' &'
					os.system(comm)
