from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../../labels/')
#methods = ['svm', 'pa', 'sgd', 'decision', 'adaboost', 'gradientboost', 'randomtrees', 'crfsuite', 'freqSimplewiki']

namem = {}
namem['svm'] = 'Support Vector Machines'
namem['pa'] = 'Passive Agressive Learning'
namem['sgd'] = 'Stochastic Gradient Descent'
namem['decision'] = 'Decision Trees'
namem['adaboost'] = 'Adaptive Boosting'
namem['gradientboost'] = 'Gradient Boosting'
namem['randomtrees'] = 'Random Forests'
namem['crfsuite'] = 'Conditional Random Fields'
namem['freqSimplewiki'] = 'Frequency: Simple Wikipedia'

bestscoring = open('best_cwi.txt', 'w')

ie = IdentifierEvaluator()

myt = []
headers = ['Method', 'Precision', 'Recall', 'F-Measure']
for method in methods:
	print(str(method))
	files = os.listdir('../../labels/'+method+'/')
	print(str(len(files)))
	maxf = -1
	maxv = []
	maxprefix = ''
	maxfile = ''
	for file in sorted(files):
		print(str(file))
		prefix = file[7:len(file)-4]
		labels = []
		f = open('../../labels/'+method+'/'+file)
		for line in f:
			try:
				labels.append(int(line.strip()))
			except Exception:
				pass
		f.close()
		try:
			p, r, f = ie.evaluateIdentifier('../../corpora/cwi_gold_standard.txt', labels)
		except Exception:
			p = 0.0
			r = 0.0
			f = 0.0
		if f>maxf:
			print(str(f))
			maxf = f
			maxv = [p, r, f]
			maxprefix = prefix
			maxfile = file
	if maxprefix!='':
		if method!='voting':
			bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
			myt.append([method, '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$'])
print(tabulate(myt, headers, tablefmt="latex"))
bestscoring.close()
