import os

folders = os.listdir('/export/data/ghpaetzold/benchmarking/cwi_separated_classes/labels/')

for folder in folders:
	path = '/export/data/ghpaetzold/benchmarking/cwi_separated_classes/labels/' + folder + '/'
	comm = 'rm ' + path + '*'
	os.system(comm)