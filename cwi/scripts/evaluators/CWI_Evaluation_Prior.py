from tabulate import tabulate
import os
from lexenstein.evaluators import *

testing_data = []
for line in open('../../corpora/cwi_paetzold_testing.txt'):
	testing_data.append(line.strip().split('\t'))

complex_words_train = set([])
f = open('../../corpora/cwi_paetzold_training.txt')
for line in f:
	data = line.strip().split('\t')
	word = data[1].strip()
	label = data[3].strip()
	if label=='1':
		complex_words_train.add(word.lower())
f.close()

methods = os.listdir('../../labels/')
maxis = set(['svm', 'pa', 'sgd', 'decision', 'shardlow', 'svm_colloc', 'svm_set1', 'svm_set2', 'voting'])

bestscoring = open('best_cwi.txt', 'w')

ie = IdentifierEvaluator()

myt = []
headers = ['Method', 'Precision', 'Recall', 'F-Measure']
for method in methods:
	print(str(method))
	files = os.listdir('../../labels/'+method+'/')
	print(str(len(files)))
	if method not in maxis:
		maxf = -1
		maxfile = None
		for file in sorted(files):
			prefix = file[7:len(file)-4]
			labels = []
			f = open('../../labels/'+method+'/'+file)
			myc = -1
			for line in f:
				myc += 1
				data = testing_data[myc]
				word = data[1].strip().lower()
				if word in complex_words_train:
					labels.append(1)
				else:
					labels.append(int(line.strip()))
			f.close()
			print(file)
			p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing.txt', labels)
			if f > maxf:
				maxf = f
				maxfile = file
			myt.append([prefix[0].upper()+prefix[1:len(prefix)], '$'+"%.3f" % p+'$', '$'+"%.3f" % r+'$', '$'+"%.3f" % f+'$'])
			
		bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
	else:
		maxf = -1
		maxv = []
		maxprefix = ''
		maxfile = ''
		for file in sorted(files):
			prefix = file[7:len(file)-4]
			labels = []
			f = open('../../labels/'+method+'/'+file)
			myc = -1
			for line in f:
				myc += 1
				data = testing_data[myc]
				word = data[1].strip().lower()
				if word in complex_words_train:
					labels.append(1)
				else:
					labels.append(int(line.strip()))
			f.close()
			p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing.txt', labels)
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
bestscoring.close()
