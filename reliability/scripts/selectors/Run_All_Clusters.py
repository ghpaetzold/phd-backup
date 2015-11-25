import os

generators = os.listdir('../../substitutions/')
generators = ['paetzold']

victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_clusters.txt'
	comm = 'nohup python Run_Clusters.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
