import os

generators = os.listdir('../../substitutions/')
generators = ['kauchak', 'paetzold', 'wordnet', 'all']

test_victor_corpus = '../../corpora/lexmturk_gold_test.txt'

#Parameters:
rs = ['1']
fs = ['10']
ts = ['0.25', '0.75']
ks = ['all']

#Run Boundary selector:
c = 0
for generator in generators:
	train_victor_corpus = '../../substitutions/all/substitutions_unsupervised.txt'
	for positive_range in rs:
		for folds in fs:
			for test_size in ts:
				for k in ks:
					c += 1
					temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
					out = '../../substitutions/'+generator+'/'
					out += 'substitutions_boundaryUnsupervisedCV_'+positive_range+'_'+folds+'_'+test_size+'_'+k
					comm = 'nohup python Run_BoundaryUnsupervisedCV.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' '
					comm += positive_range+' '+folds + ' ' + test_size +' 0 '
					comm += '0 0 0 0 ' + k + ' ' + temp_file + ' ' + out + ' &'
					os.system(comm)
