import os

flabels = []
flabels.append('subimdb22')

generators = os.listdir('../../substitutions/')
generators = ['all', 'kauchak', 'paetzold', 'wordnet']
proportions = ['7', '14']

for generator in generators:
		test_victor_corpus = '../../substitutions/'+generator+'/substitutions_unsupervised.txt'
		for proportion in proportions:
			for i in range(0, len(flabels)):
				output = '../../substitutions/'+generator+'/substitutions_'+flabels[i]+'_'+proportion+'.txt'
				comm = 'nohup python Run_Metric.py ' + test_victor_corpus+' '+str(i)+' '+output+' '+proportion+' &'
				os.system(comm)
