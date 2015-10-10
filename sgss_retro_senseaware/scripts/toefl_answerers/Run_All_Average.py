import os

types = ['TEM', 'REM', 'SEM', 'RSEM']
sizes = ['500']
#sizes = ['700']
archs = ['cbow', 'skip']

for type in types:
	for size in sizes:
		for arch in archs:
			comm = 'nohup python Run_Average.py ' + type + ' ' + size + ' ' + arch + ' &'
			os.system(comm)
