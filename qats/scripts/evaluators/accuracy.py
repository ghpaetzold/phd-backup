import os
from tabulate import tabulate

def getAccuracy(pred, gold):
	right = 0.0
	for i in range(0, len(pred)):
		if pred[i]==gold[i]:
			right += 1.0
	return right/len(pred)

types = ['G', 'M', 'S', 'O']

f = open('best_accuracy.txt', 'w')
for type in types:
	print('\n' + type + ':')
	table = []
	gold = [item.strip().split('\t')[2] for item in open('../../corpora/'+type+'_test.txt')]
	systems = sorted(os.listdir('../../labels/'+type))
	for system in systems:
		files = os.listdir('../../labels/'+type+'/'+system)
		maxacc = -1
		maxfile = None
		for file in files:
			pred = [item.strip().split('\t')[0] for item in open('../../labels/'+type+'/'+system+'/'+file)]
			acc = getAccuracy(pred, gold)
			if acc>maxacc:
				maxacc = acc
				maxfile = file
		if maxfile:
			table.append([system, maxacc])
			f.write(type + '\t' + system + '\t' + maxfile + '\n')
	print(tabulate(table, headers=['System', 'Accuracy']))
f.close()
