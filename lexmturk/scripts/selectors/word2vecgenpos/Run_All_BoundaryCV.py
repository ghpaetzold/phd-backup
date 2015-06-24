import os

proportions = ['0.125', '0.25', '0.5']

generators = os.listdir('../../../substitutions/')
victor_corpus = '../../../corpora/lexmturk_all_targetfirst.txt'

#Run Boundary selector:
c = 0
for generator in generators:
	for proportion in proportions:
		c += 1
		temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
		out = '../../../substitutions/'+generator+'/'
		out += 'substitutions_boundaryCV_'+proportion+'_posw2v.txt'
		comm = 'nohup python Run_Boundary.py ' + generator + ' ' + victor_corpus + ' 1  0 '
		comm += '0 0 0 0 ' + temp_file + ' ' + proportion + ' ' + out + ' 1 &'
		os.system(comm)
