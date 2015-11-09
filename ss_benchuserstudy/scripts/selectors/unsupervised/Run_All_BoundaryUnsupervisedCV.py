import os

generators = os.listdir('../../../substitutions/')
generators = ['all']

test_victor_corpus = '../../../corpora/ss_dataset_userstudy_final.txt'

#Parameters:
rs = ['1']
fs = ['10']
ts = ['0.25']
ks = ['all']
ks = ['8']
proportions = ['0.25'] 

#Run Boundary selector:
c = 0
for generator in generators:
	train_victor_corpus = '../../../substitutions/all/substitutions_unsupervised.txt'
	for proportion in proportions:
		for positive_range in rs:
			for folds in fs:
				for test_size in ts:
					for k in ks:
						c += 1
						temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
						out = '../../../substitutions/'+generator+'/'
						out += 'substitutions_boundaryUnsupervisedCV_'+proportion+'_'+positive_range+'_'+folds+'_'+test_size+'_'+k+'nopos.txt'
						comm = 'nohup python Run_BoundaryUnsupervisedCV.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' '
						comm += positive_range+' '+folds + ' ' + test_size +' 0 '
						comm += '0 0 0 0 ' + k + ' ' + temp_file + ' ' + proportion + ' ' + out + ' &'
						os.system(comm)
