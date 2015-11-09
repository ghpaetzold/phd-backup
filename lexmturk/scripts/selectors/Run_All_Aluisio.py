import os

generators = os.listdir('../../substitutions/')
generators = ['all']

victor_corpus = '../../corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_aluisio.txt'
	comm = 'nohup python Run_Aluisio.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
