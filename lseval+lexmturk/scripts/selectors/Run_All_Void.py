import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/ls_dataset_benchmarking.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_void.txt'
	comm = 'nohup python Run_Void.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
