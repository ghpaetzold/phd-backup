import os

trainset = '../../corpora/NNSimpLex_train.txt'
testset = '../../corpora/NNSimpLex_test.txt'
os.system('mkdir ../../rankings/biran/')

output = '../../rankings/biran/ranks_biran.txt'
clm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
slm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
os.system(comm)
#print(comm)
