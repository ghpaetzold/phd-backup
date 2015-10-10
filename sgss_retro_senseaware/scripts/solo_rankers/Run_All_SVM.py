import os

#Parameters:
Cs = ['1']
epsilons = ['0.0001']
kernels = ['0', '2']
types = ['TEM', 'REM', 'SEM', 'RSEM']
size = '500'
archs = ['cbow', 'skip']

trainset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_train_clean.txt'
testset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt'
counter = -1
for C in Cs:
	for e in epsilons:
		for k in kernels:
			for type in types:
				for arch in archs:
					os.system('mkdir ../../solo_rankings/svm/')
					os.system('mkdir ../../solo_rankings/svm/' + type)
					os.system('mkdir ../../solo_rankings/svm/' + type + '/' + arch)
					os.system('mkdir ../../solo_rankings/svm/' + type + '/' + arch + '/' + size)
					counter += 1
					output = '../../solo_rankings/svm/' + type + '/' + arch + '/' + size + '/ranks_'+C+'_'+e+'_'+k+'.txt'
					trfile = './temp/train_feature_file_'+str(counter)+'.txt'
					mfile = './temp/model_'+str(counter)+'.txt'
					tefile = './temp/test_feature_file_'+str(counter)+'.txt'
					sfile = './temp/scores_'+str(counter)+'.txt'
					comm = 'nohup python Run_SVMRank.py '+trainset+' '+trfile+' '+C+' '+e+' '+k+' '+mfile+' '
					comm += tefile+' '+sfile+' '+testset+' '+output+' '+type + ' ' + size + ' ' + arch + ' &'
					os.system(comm)
