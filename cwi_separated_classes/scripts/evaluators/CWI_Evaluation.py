from tabulate import tabulate
import os
from lexenstein.evaluators import *

def getAllClasses():
	path = '../../labels/decision/'
	files = os.listdir(path)
	result = set([])
	for file in files:
		c = file.strip()[0:len(file)-4].split('_')
		c = c[len(c)-1]
		result.add(c)
	return result

methods = os.listdir('../../labels/')
maxis = set(['svm', 'pa', 'sgd', 'decision', 'shardlow', 'svm_colloc', 'svm_set1', 'svm_set2', 'voting'])

bestscoring = open('best_cwi.txt', 'w')

ie = IdentifierEvaluator()

classes = getAllClasses()
headers = ['Method', 'Precision', 'Recall', 'F-Measure']

for wclass in classes:
	myt = []
	print('\nClass: ' + wclass)
	for method in methods:
		files = os.listdir('../../labels/'+method+'/')
		if method not in maxis:
			maxf = -1
			maxfile = None
			for file in sorted(files):
				if wclass+'.txt' in file:
					prefix = file[7:len(file)-4]
					labels = []
					f = open('../../labels/'+method+'/'+file)
					for line in f:
						labels.append(int(line.strip().split('\t')[0].strip()))
					f.close()
					p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing_'+wclass+'.txt', labels)
					if f > maxf:
						maxf = f
						maxfile = file
					myt.append([prefix[0].upper()+prefix[1:len(prefix)], '$'+"%.3f" % p+'$', '$'+"%.3f" % r+'$', '$'+"%.3f" % f+'$'])
				if maxfile:		
					bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
		else:
			maxf = -1
			maxv = []
			maxprefix = ''
			maxfile = ''
			for file in sorted(files):
				if wclass+'.txt' in file:
					prefix = file[7:len(file)-4]
					labels = []
					f = open('../../labels/'+method+'/'+file)
					for line in f:
						labels.append(int(line.strip().split('\t')[0].strip()))
					f.close()
					p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing_'+wclass+'.txt', labels)
					if f>maxf:
						maxf = f
						maxv = [p, r, f]
						maxprefix = prefix
						maxfile = file
			if maxprefix!='':
	#			if method!='voting':
				bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
				myt.append([maxprefix, '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$'])
	print(tabulate(myt, headers, tablefmt="latex"))
