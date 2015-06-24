import os

test_victor_corpus = '../../corpora/lexmturk_nosupervision_test.txt'

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

generators = os.listdir('../../substitutions/')

for generator in generators:
		for i in range(0, len(flabels)):
			output = '../../substitutions/'+generator+'/substitutions_'+flabels[i]+'.txt'
			comm = 'nohup python Run_Metric.py ' + test_victor_corpus+' '+str(i)+' '+output+' &'
			os.system(comm)
