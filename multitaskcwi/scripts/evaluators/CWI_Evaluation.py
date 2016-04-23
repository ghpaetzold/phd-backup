from tabulate import tabulate
import os
from lexenstein.evaluators import *

tasks = os.listdir('../../labels/')

methods = os.listdir('../../labels/' + tasks[0])
#methods = ['svm', 'pa', 'sgd', 'decision', 'adaboost', 'gradientboost', 'randomtrees', 'crfsuite', 'freqSimplewiki', 'freqWiki', 'freqSubimdb', 'freqSubtlex', 'freqSubimdblex', 'nn']
#methods.extend(['length','senses','hypernyms','hyponyms','voting','votinghard','all','none','lex_Ogdens','lex_SimpleWikipedia','lex_Wikipedia','lex_Stop','lex_SubIMDB'])
#methods = ['softvoting']

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
namem['synonyms'] = 'Number of Synonyms'
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
namem['softvoting'] = 'Traditional Soft Voting'

ie = IdentifierEvaluator()

for task in tasks:
	print(task + ':')

	myt = []
	headers = ['Method', 'Accuracy', 'Precision', 'Recall', 'F-score', 'G-score']
	for method in methods:
		files = os.listdir('../../labels/'+task+'/'+method+'/')
		maxg = -1
		maxv = [0.0, 0.0, 0.0, 0.0, 0.0]
		maxprefix = ''
		maxfile = ''
		for file in sorted(files):
			prefix = file[7:len(file)-4]
			labels = []
			f = open('../../labels/'+task+'/'+method+'/'+file)
			for line in f:
				try:
					labels.append(int(line.strip()))
				except Exception:
					pass
			f.close()
			try:
				a, p, r, f, g = ie.evaluateIdentifier('../../corpora/cwi_testing_multitask_decomposed.txt', labels)
			except Exception:
				a = 0.0
				p = 0.0
				r = 0.0
				f = 0.0
				g = 0.0
			if g>maxg:
				print('better!')
				maxg = g
				maxv = [a, p, r, f, g]
				maxprefix = prefix
				maxfile = file
		if method!='voting':
			myt.append([namem[method], r'$'+"%.3f" % maxv[0]+r'$', r'$'+"%.3f" % maxv[1]+r'$', r'$'+"%.3f" % maxv[2]+r'$', r'$'+"%.3f" % maxv[3]+r'$', r'$'+"%.3f" % maxv[4]+r'$'])
		else:
			myt.append([namem[method], '$'+"%.3f" % maxv[0]+'$', '$'+"%.3f" % maxv[1]+'$', '$'+"%.3f" % maxv[2]+'$', '$'+"%.3f" % maxv[3]+'$', '$'+"%.3f" % maxv[4]+'$'])
	print(tabulate(myt, headers, tablefmt="latex"))
	print('')