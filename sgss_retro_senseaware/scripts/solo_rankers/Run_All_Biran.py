import os

trainset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_train_clean.txt'
testset = '/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt'

os.system('mkdir ../../solo_rankings/biran/')

output = '../../solo_rankings/biran/ranks_biran.txt'
clm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
slm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
os.system(comm)
#print(comm)
