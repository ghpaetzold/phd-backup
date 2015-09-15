import os

#Parameters:
alphas = ['1']

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/yamamoto')

for a1 in alphas:
	for a2 in alphas:
		for a3 in alphas:
			for a4 in alphas:
				for a5 in alphas:
					output = '../../sr_rankings/yamamoto/ranks_'+a1+'_'+a2+'_'+a3+'_'+a4+'_'+a5+'.txt'
					lm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
					cooc = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/vectors.clean.txt'
					comm = 'nohup python Run_Yamamoto.py '+trainset+' '+lm+' '+cooc+' '+a1+' '+a2+' '+a3+' '+a4+' '+a5+' '+testset+' '+output+' &'
					os.system(comm)
					#print(comm)
