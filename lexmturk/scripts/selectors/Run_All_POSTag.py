import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_postag.txt'
	comm = 'nohup python Run_POSTag.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
