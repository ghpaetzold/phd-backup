import os

#Datasets:
datasets = ['SCWS-2003', 'MEN-3000']
types = ['TEM', 'REM', 'SEM', 'RSEM']
sizes = ['500']
archs = ['cbow', 'skip']

for dataset in datasets:
	for type in types:
		for size in sizes:
			for arch in archs:
				comm = 'nohup python Run_Tagged.py ' + dataset + ' ' + type + ' ' + size + ' ' + arch + ' &'
				os.system(comm)
