from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../../labels_majority/')
methods = ['decision', 'shardlow', 'threshold', 'lexicon', 'none', 'all']
maxis = set(['decision', 'shardlow'])
#maxis = set(['svm', 'pa', 'sgd', 'decision', 'shardlow', 'svm_colloc', 'svm_set1', 'svm_set2'])

ie = IdentifierEvaluator()

myt = []
headers = ['Method', 'Precision', 'Recall', 'F-Measure']
for method in methods:
	files = os.listdir('../../labels_majority/'+method+'/')
	if method not in maxis:
		for file in sorted(files):
			prefix = file[7:len(file)-4]
			labels = []
			f = open('../../labels_majority/'+method+'/'+file)
			for line in f:
				labels.append(int(line.strip()))
			f.close()
			print(file)
			p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing.txt', labels)
			myt.append([prefix[0].upper()+prefix[1:len(prefix)], '$'+"%.3f" % p+'$', '$'+"%.3f" % r+'$', '$'+"%.3f" % f+'$'])
	else:
		maxf = -1
		maxv = []
		prefix = ''
		for file in sorted(files):
			prefix = file[7:len(file)-4]
			labels = []
			f = open('../../labels_majority/'+method+'/'+file)
			for line in f:
				labels.append(int(line.strip()))
			f.close()
			print('File: ' + file)
			p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing.txt', labels)
			if f>maxf:
				maxf = f
				maxv = [p, r, f]
		if prefix!='':
			myt.append([prefix, '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$'])
print(tabulate(myt, headers, tablefmt="latex"))
