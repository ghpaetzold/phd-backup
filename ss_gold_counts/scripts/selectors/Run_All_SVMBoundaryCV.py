import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_gold_targetfirst.txt'

#Parameters:
rs = ['1', '2']
fs = ['3', '5', '10']
ts = ['0.25', '0.50', '0.75']
proportions = ['1.0']

#Run Boundary selector:
c = 0
for generator in generators:
	for proportion in proportions:
		for positive_range in rs:
			for folds in fs:
				for test_size in ts:
					c += 1
					temp_file = './temp/temp_file_svmboundary_' + str(c) + '.txt'
					out = '../../substitutions/'+generator+'/'
					out += 'substitutions_svmboundaryCV_'+proportion+'_'+positive_range+'_'+folds+'_'+test_size+'.txt'
					comm = 'nohup python Run_SVMBoundaryCV.py ' + generator + ' ' + victor_corpus + ' '+positive_range+' '+folds + ' ' + test_size
					comm += ' ' + temp_file + ' ' + proportion + ' ' + out + ' &'
					os.system(comm)