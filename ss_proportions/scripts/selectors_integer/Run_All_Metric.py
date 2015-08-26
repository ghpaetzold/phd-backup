import os

flabels = []
flabels.append('subimdb22')

generators = os.listdir('../../substitutions/')
generators = ['all', 'kauchak', 'paetzold', 'wordnet']

for generator in generators:
		test_victor_corpus = '../../substitutions/'+generator+'/substitutions_unsupervised_test.txt'
		for i in range(0, len(flabels)):
			output = '../../substitutions/'+generator+'/substitutions_'+flabels[i]
			comm = 'nohup python Run_Metric.py ' + test_victor_corpus+' '+str(i)+' '+output+' &'
			os.system(comm)
