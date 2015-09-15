import os

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/glavas')

output = '../../sr_rankings/glavas/ranks_glavas.txt'
comm = 'nohup python Run_Glavas.py '+trainset+' '+testset+' '+output+' &'
os.system(comm)
