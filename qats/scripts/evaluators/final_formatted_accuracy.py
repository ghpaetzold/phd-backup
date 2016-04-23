import os
from tabulate import tabulate
from scipy.stats import pearsonr

def getAccuracy(pred, gold):
	right = 0.0
	for i in range(0, len(pred)):
		if pred[i]==gold[i]:
			right += 1.0
	return right/len(pred)

types = ['G', 'M', 'S', 'O']

systems = sorted(os.listdir('../../finallabels/G'))
names = {}
names['rnn3'] = 'SimpleNets-RNN3'
names['rnn2'] = 'SimpleNets-RNN2'
names['nn_mlp_final'] = 'SimpleNets-MLP'
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
	gold = [item.strip().split('\t')[2] for item in open('../../corpora/testset/'+type+'_all_with_labels.txt')]
	golds = [float(item.strip().split('\t')[2]) for item in open('../../corpora/testset/'+type+'_all_with_labels.txt')]
	for system in systems:
		files = os.listdir('../../finallabels/'+type+'/'+system)
		maxacc = -1
		maxspear = 0
		maxfile = None
		for file in files:
			pred = [item.strip().split('\t')[0] for item in open('../../finallabels/'+type+'/'+system+'/'+file)]
			preds = [float(item.strip().split('\t')[1]) for item in open('../../finallabels/'+type+'/'+system+'/'+file)]
			preds[0] = preds[0]+0.00000001
			acc = getAccuracy(pred, gold)
			if acc>maxacc:
				maxacc = acc
				maxfile = file
			spear, f = pearsonr(preds, golds)
			print(str(spear))
			if acc>maxspear:
				maxspear = spear
		scores[system].append((maxacc*100, maxspear))

for system in sorted(scores.keys()):
	if system in names:
		newline = names[system]
		for value in scores[system]:
			newline += r' & $' + "%.2f" % value[0] + r'$ & $' + "%.3f" % value[1] + r'$'
		newline += r' \\'
		print(newline)

#Print results from task:
systems = {}
for type in types:
	print(type)
	f = open('../../corpora/taskresults/'+type+'_acc.txt')
	f.readline()
	for line in f:
		token = line.strip().split('\t')[0]
		token = token.strip().split(' ')[1]
		systems[token] = {}
	f.close()
	f = open('../../corpora/taskresults/'+type+'_p.txt')
	f.readline()
	for line in f:
	        token = line.strip().split('\t')[0]
	        token = token.strip().split(' ')[1]
	        systems[token] = {}
	f.close()

for type in types:
	f = open('../../corpora/taskresults/'+type+'_acc.txt')
	f.readline()
	for line in f:
	        token = line.strip().split('\t')[0]
	        token = token.strip().split(' ')
	        systems[token[1]][type+'_acc'] = token[0]
	f.close()
	f = open('../../corpora/taskresults/'+type+'_p.txt')
        f.readline()
        for line in f:
                token = line.strip().split('\t')[0]
                token = token.strip().split(' ')
                systems[token[1]][type+'_p'] = token[0]
        f.close()

print('')
for system in sorted(systems.keys()):
	newline = system
	for type in types:
		if type+'_acc' in systems[system]:
			newline += ' & $' + systems[system][type+'_acc'] + '$'
		else:
			newline += ' & -'
		if type+'_p' in systems[system]:
                        newline += ' & $' + systems[system][type+'_p'] + '$'
		else:
                        newline += ' & -'		
	print(newline + r' \\')
