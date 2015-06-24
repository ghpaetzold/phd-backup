import os

folders = os.listdir('/export/data/ghpaetzold/benchmarking/cwi/labels/')

for folder in folders:
	path = '/export/data/ghpaetzold/benchmarking/cwi/labels/' + folder + '/'
	comm = 'rm ' + path + '*'
	os.system(comm)
