import os

folders = os.listdir('/export/data/ghpaetzold/benchmarking/cwi_classes/labels/')

for folder in folders:
	path = '/export/data/ghpaetzold/benchmarking/cwi_classes/labels/' + folder + '/'
	comm = 'rm ' + path + '*'
	os.system(comm)
