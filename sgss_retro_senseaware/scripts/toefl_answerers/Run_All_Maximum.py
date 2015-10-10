import os

types = ['TEM', 'REM', 'SEM', 'RSEM']
types = ['SEM', 'RSEM']
sizes = ['500']
archs = ['cbow', 'skip']

for type in types:
	for size in sizes:
		for arch in archs:
			comm = 'nohup python Run_Maximum.py ' + type + ' ' + size + ' ' + arch + ' &'
			os.system(comm)
