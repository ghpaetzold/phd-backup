import os

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'

output = '../rankings/biran/ranks_biran.txt'
clm = '../../lexmturk/corpora/wiki.5gram.bin.txt'
slm = '../../../machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
os.system(comm)
#print(comm)
