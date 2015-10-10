import os

types = ['TEM', 'REM', 'SEM', 'RSEM']
size = '500'
archs = ['cbow', 'skip']

for type in types:
	for arch in archs:
		os.system('mkdir ../../solo_rankings/glavas/')
		os.system('mkdir ../../solo_rankings/glavas/' + type)
		os.system('mkdir ../../solo_rankings/glavas/' + type + '/' + arch)
		os.system('mkdir ../../solo_rankings/glavas/' + type + '/' + arch + '/' + size)
                output = '../../solo_rankings/glavas/' + type + '/' + arch + '/' + size + '/ranks_glavas.txt'
		trainset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_train_clean.txt'
		testset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt'
		comm = 'nohup python Run_Glavas.py '+trainset+' '+testset+' '+output + ' ' + type + ' ' + size + ' ' + arch + ' &'
		os.system(comm)
