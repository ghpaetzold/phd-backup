import os

generators = os.listdir('../../substitutions/')
generators = ['kauchak', 'paetzold', 'wordnet']

#train_victor_corpus = '../../corpora/lexmturk_gold_targetfirst_train.txt'
test_victor_corpus = '../../corpora/lexmturk_gold_test.txt'

#Parameters:
rs = ['1']
fs = ['5', '10']
ts = ['0.25', '0.75']
ks = ['8', 'all']
proportions = ['1.0']

#Run Boundary selector:
c = 0
for generator in generators:
	train_victor_corpus = '../../substitutions/'+generator+'/substitutions_unsupervised.txt'
	for proportion in proportions:
		for positive_range in rs:
			for folds in fs:
				for test_size in ts:
					for k in ks:
						c += 1
						temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
						out = '../../substitutions/'+generator+'/'
						out += 'substitutions_boundaryUnsupervisedCV_'+proportion+'_'+positive_range+'_'+folds+'_'+test_size+'_'+k+'.txt'
						comm = 'nohup python Run_BoundaryUnsupervisedCV.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' '
						comm += positive_range+' '+folds + ' ' + test_size +' 0 '
						comm += '0 0 0 0 ' + k + ' ' + temp_file + ' ' + proportion + ' ' + out + ' &'
						os.system(comm)
