import os
from tabulate import tabulate
from scipy.stats import spearmanr

def getAccuracy(pred, gold):
	right = 0.0
	for i in range(0, len(pred)):
		if pred[i]==gold[i]:
			right += 1.0
	return right/len(pred)

types = ['G', 'M', 'S', 'O']

systems = sorted(os.listdir('../../labels/G'))
names = {}
names['nn'] = 'SimpleNets-RNN3'
names['nn_adadelta'] = 'SimpleNets-RNN2'
names['nn_mlp'] = 'SimpleNets-MLP'
names['adaboost'] = 'Ada Boosting'
names['dectrees'] = 'Decision Trees'
names['gradientboost'] = 'Gradient Boosting'
names['randomforest'] = 'Random Forests'
names['sgd'] = 'SGD'
names['svm'] = 'SVM'
names['allgood'] = 'All Good'
names['allok'] = 'All Ok'
names['allbad'] = 'All Bad'

scores = {}
for system in systems:
	scores[system] = []

for type in types:
	gold = [item.strip().split('\t')[2] for item in open('../../corpora/'+type+'_test.txt')]
	golds = [float(item.strip().split('\t')[2]) for item in open('../../corpora/'+type+'_test.txt')]
	for system in systems:
		files = os.listdir('../../labels/'+type+'/'+system)
		maxacc = -1
		maxspear = 0
		maxfile = None
		for file in files:
			pred = [item.strip().split('\t')[0] for item in open('../../labels/'+type+'/'+system+'/'+file)]
			preds = [float(item.strip().split('\t')[1]) for item in open('../../labels/'+type+'/'+system+'/'+file)]
			preds[0] = preds[0]+0.00000001
			acc = getAccuracy(pred, gold)
			if acc>maxacc:
				maxacc = acc
				maxfile = file
			spear, f = spearmanr(preds, golds)
			if acc>maxspear:
				maxspear = spear
		scores[system].append((maxacc, maxspear))

for system in sorted(scores.keys()):
	if system in names:
		newline = names[system]
		for value in scores[system]:
			newline += r' & $' + "%.3f" % value[0] + r'$ & $' + "%.3f" % value[1] + r'$'
		newline += r' \\'
		print(newline)
