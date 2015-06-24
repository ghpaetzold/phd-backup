import os

generators = os.listdir('../../substitutions/')
generators = ['kauchak']
victor_corpus = '../../corpora/lexmturk_all_targetfirst.txt'

#Parameters:
rs = ['1']
fs = ['5', '10']
ts = ['0.25', '0.50', '0.75']
proportions = ['0.125', '0.25', '0.5']
ks = ['2', '3', '6', '7']

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
						comm = 'nohup python Run_BoundaryCV.py ' + generator + ' ' + victor_corpus + ' '+positive_range+' '+folds + ' ' + test_size +' 0 '
						comm += '0 0 0 0 ' + temp_file + ' ' + proportion + ' ' + k + ' ' + out + ' &'
						os.system(comm)
print(str(c))
