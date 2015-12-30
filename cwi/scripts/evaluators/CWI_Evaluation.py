from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../../labels/')
methods = ['svm', 'pa', 'sgd', 'decision', 'adaboost', 'gradientboost', 'randomtrees', 'crfsuite', 'freqSimplewiki', 'freqWiki', 'freqSubimdb', 'freqSubtlex', 'freqSubimdblex', 'nn']
methods.extend(['length','senses','hypernyms','hyponyms','voting','votinghard','all','none','lex_Ogdens','lex_SimpleWikipedia','lex_Wikipedia','lex_Stop','lex_SubIMDB'])

#methods = ['nn']

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
namem['freqSubimdb'] = 'Frequency: SubIMDB'
namem['freqSubtlex'] = 'Frequency: SUBTLEX'
namem['freqSubimdblex'] = 'Frequency: SubIMDBLEX'
namem['freqWiki'] = 'Frequency: Wikipedia'
namem['length'] = 'Length'
namem['senses'] = 'Number of Senses'
namem['hypernyms'] = 'Number of Hypernyms'
namem['hyponyms'] = 'Number of Hyponyms'
namem['mindepth'] = 'Minimum Depth'
namem['maxdepth'] = 'Maximum Depth'
namem['nn'] = 'Neural Networks'
namem['voting'] = 'Voting'
namem['votinghard'] = 'Hard Voting'
namem['all'] = 'All Complex'
namem['none'] = 'All Simple'
namem['lex_Ogdens'] = r'Lexicon: Ogdens'
namem['lex_SimpleWikipedia'] = r'Lexicon: Simple Wikipedia'
namem['lex_Wikipedia'] = r'Lexicon: Wikipedia'
namem['lex_Stop'] = r'Lexicon: Stop Words'
namem['lex_SubIMDB'] = r'Lexicon: SubIMDB'

bestscoring = open('best_cwi.txt', 'w')

ie = IdentifierEvaluator()

myt = []
headers = ['Method', 'Accuracy', 'Precision', 'Recall', 'F-Measure']
for method in methods:
	print(str(method))
	files = os.listdir('../../labels/'+method+'/')
	print(str(len(files)))
	maxf = -1
	maxv = []
	maxprefix = ''
	maxfile = ''
	for file in sorted(files):
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
			a, p, r, f = ie.evaluateIdentifier('../../corpora/cwi_paetzold_testing.txt', labels)
		except Exception:
			a = 0.0
			p = 0.0
			r = 0.0
			f = 0.0
		if f>maxf:
			print(str(f))
			maxf = f
			maxv = [a, p, r, f]
			maxprefix = prefix
			maxfile = file
	if method!='voting':
		bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
		myt.append([namem[method], '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$', '$'+"%.3f" % maxv[3]+'$'])
	else:
		bestscoring.write(method + '\t' + maxfile + '\t' + str(maxf) + '\n')
		myt.append([namem[method], '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$', '$'+"%.3f" % maxv[3]+'$'])
print(tabulate(myt, headers, tablefmt="latex"))
bestscoring.close()
