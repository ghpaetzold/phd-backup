import os

generators = os.listdir('../../substitutions/')

victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

#Run WSD selector:
methods = ['lesk', 'path', 'random', 'first']
for generator in generators:
	for method in methods:
		out = '../../substitutions/'+generator+'/'
		out += 'substitutions_'+method+'.txt'
		comm = 'nohup python Run_WSD.py '+generator+' '+victor_corpus+' '+method+' '+out+' &'
		os.system(comm)
