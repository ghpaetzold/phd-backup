import os
from tabulate import tabulate
from scipy.stats import spearmanr
import numpy as np

types = ['G', 'M', 'S', 'O']

for type in types:
	print('\n' + type + ':')
	table = []
	gold = [float(item.strip().split('\t')[2]) for item in open('../../corpora/'+type+'_test.txt')]
	systems = sorted(os.listdir('../../labels/'+type))
	for system in systems:
		files = os.listdir('../../labels/'+type+'/'+system)
		maxacc = -1
		for file in files:
			pred = [float(item.strip().split('\t')[1]) for item in open('../../labels/'+type+'/'+system+'/'+file)]
			pred[0] = pred[0]+0.00001
			#print(str(pred))
			acc, f = spearmanr(pred, gold)
			if acc>maxacc:
				maxacc = acc
		table.append([system, maxacc])
	print(tabulate(table, headers=['System', 'Spearman']))
