import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../../lexmturk/corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_void.txt'
	comm = 'nohup python Run_Void.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
