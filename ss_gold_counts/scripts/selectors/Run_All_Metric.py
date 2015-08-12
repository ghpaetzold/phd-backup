import os

flabels = []
flabels.append('vectorsim')
flabels.append('subimdb10')
flabels.append('subimdb01')
flabels.append('subimdb11')
flabels.append('subimdb20')
flabels.append('subimdb02')
flabels.append('subimdb21')
flabels.append('subimdb12')
flabels.append('subimdb22')
flabels.append('translationprob')
flabels.append('postagprob')

generators = os.listdir('../../substitutions/')
generators = ['all', 'kauchak', 'paetzold', 'wordnet']

for generator in generators:
		test_victor_corpus = '../../substitutions/'+generator+'/substitutions_unsupervised_test.txt'
		for i in range(0, len(flabels)):
			output = '../../substitutions/'+generator+'/substitutions_'+flabels[i]+'.txt'
			comm = 'nohup python Run_Metric.py ' + test_victor_corpus+' '+str(i)+' '+output+' &'
			os.system(comm)
