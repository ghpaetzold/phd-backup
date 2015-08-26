import os

generators = os.listdir('../../substitutions/')
generators = ['wordnet', 'kauchak', 'paetzold']
generators = ['kauchak']

train_victor_corpus = '../../corpora/lexmturk_all.txt'

test_victor_corpus = '../../corpora/lexmturk_all.txt'

#Parameters:
rs = ['1', '2', '3']
fs = ['5', '10']
ts = ['0.5']
ks = ['all']
proportions = ['5', '7']

#Run Boundary selector:
c = 0
for generator in generators:
	for proportion in proportions:
		for positive_range in rs:
			for folds in fs:
				for test_size in ts:
					for k in ks:
						c += 1
						temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
						out = '../../substitutions/'+generator+'/'
						out += 'substitutions_boundaryCV_'+proportion+'_'+positive_range+'_'+folds+'_'+test_size+'_'+k+'.txt'
						comm = 'nohup python Run_BoundaryCV.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' '
						comm += positive_range+' '+folds + ' ' + test_size +' 0 '
						comm += '0 0 0 0 ' + k + ' ' + temp_file + ' ' + proportion + ' ' + out + ' &'
						os.system(comm)
