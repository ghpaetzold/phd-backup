import os

#Datasets:
#datasets = ['WS-353', 'RG-65']
#datasets = ['MC-30', 'MEN-3000', 'SCWS-2003', 'MT-287']
#datasets = ['MC-30', 'MEN-3000']
datasets = ['SCWS-2003', 'MT-287']
#datasets = ['SCWS-2003']
types = ['TEM', 'REM', 'SEM', 'RSEM']
sizes = ['500']
archs = ['cbow', 'skip']

for dataset in datasets:
	for type in types:
		for size in sizes:
			for arch in archs:
				comm = 'nohup python Run_Maximum.py ' + dataset + ' ' + type + ' ' + size + ' ' + arch + ' &'
				os.system(comm)
