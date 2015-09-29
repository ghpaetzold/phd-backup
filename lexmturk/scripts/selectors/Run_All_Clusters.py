import os

generators = os.listdir('../../substitutions/')
generators = ['paetzold', 'glavas', 'glavas_retrofitted', 'paetzold_retrofitted']

victor_corpus = '../../corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_clusters.txt'
	comm = 'nohup python Run_Clusters.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
