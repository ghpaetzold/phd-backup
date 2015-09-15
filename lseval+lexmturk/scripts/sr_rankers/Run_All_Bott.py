import os

#Parameters:
alphas = ['1']

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/bott')
for a1 in alphas:
	for a2 in alphas:
		output = '../../sr_rankings/bott/ranks_'+a1+'_'+a2+'.txt'
		lm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
		comm = 'nohup python Run_Bott.py '+trainset+' '+lm+' '+a1+' '+a2+' '+testset+' '+output+' &'
		os.system(comm)
		#print(comm)
