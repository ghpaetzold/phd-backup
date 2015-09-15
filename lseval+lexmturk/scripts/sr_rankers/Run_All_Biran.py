import os

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/biran')

output = '../../sr_rankings/biran/ranks_biran.txt'
clm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
slm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
os.system(comm)
#print(comm)
