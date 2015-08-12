import os

generators = os.listdir('../../substitutions/')
generators = ['kauchak+paetzold', 'paetzold+wordnet', 'kauchak+paetzold+wordnet']

victor_corpus = '../../corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_void.txt'
	comm = 'nohup python Run_Void.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
