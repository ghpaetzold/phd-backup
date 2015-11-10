import os

testset = '../../corpora/NNSimpLex_test.txt'

comm = 'nohup python Run_Metric.py '+testset+' &'
os.system(comm)
