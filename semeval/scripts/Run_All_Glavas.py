import os

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'

os.system('mkdir ../rankings/glavas')

output = '../rankings/glavas/ranks_glavas.txt'
comm = 'nohup python Run_Glavas.py '+trainset+' '+testset+' '+output+' &'
os.system(comm)
