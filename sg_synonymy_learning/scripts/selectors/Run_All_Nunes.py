import os

generators = os.listdir('../../substitutions/')
generators = ['all']

victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_nunes.txt'
	comm = 'nohup python Run_Nunes.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
