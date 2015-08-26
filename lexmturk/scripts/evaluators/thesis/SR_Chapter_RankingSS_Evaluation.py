from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Generators:
generators = ['wordnet', 'kauchak', 'paetzold', 'all']

#Selectors:
selectors = ['first', 'random', 'lesk', 'wupalmer', 'biran', 'clusters', 'subimdb22', 'boundaryCV', 'boundaryUnsupervisedCV', 'svmrank', 'void']

#Linebreakers:
linebreakers = ['clusters', 'svmrank']

#Rankers:
methods = ['length', 'colloc00', 'senses', 'synonyms', 'hypernyms', 'hyponyms']

#Names:
namem = {}
namem['void'] = 'No Selection'
namem['lesk'] = 'Lesk'
namem['first'] = 'First'
namem['random'] = 'Random'
namem['wupalmer'] = 'Leacock'
namem['biran'] = 'Biran'
namem['clusters'] = 'Brown'
namem['boundaryCV'] = 'Supervised Boundary'
namem['boundaryUnsupervisedCV'] = 'Unsupervised Boundary'
namem['svmrank'] = 'SVM Rank'
namem['subimdb22'] = 'Metric-Based'

results = {}
for generator in generators:
	results[generator] = {}
	for selector in selectors:
		results[generator][selector] = {}
		for method in methods:
			results[generator][selector][method] = (-1.0, -1.0, -1.0)

pe = PipelineEvaluator()
for method in methods:
		#print(method)
		files = os.listdir('../../../rankings/'+method+'/')

		for file in files:
			filed = file.strip().split('.')[0].strip().split('_')
			generator = filed[1].strip()
			selector = filed[2].strip()

			subs = []
			f = open('../../../rankings/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			
			precision, accuracy, changed = pe.evaluatePipeline('../../../corpora/lexmturk_all.txt', subs)
			
			if generator in generators and selector in selectors and method in methods:
				if precision>results[generator][selector][method][0]:
					results[generator][selector][method] = (precision, accuracy, changed)

index = -1
for method in methods:
	index += 1
	myt = ''
	myt += r'\begin{table}[htpb]'+'\n'
	myt += r'\caption{Accuracy scores for candidate substitutions ranked by their number of ' + method + '}\n'
	myt += r'\centering'+'\n'
	myt += r'\label{table:ssrankrndtrp'+str(index)+'}\n'
	myt += r'\begin{tabular}{l|cccc}'+'\n'
	myt += r' & WordNet & Kauchak & Paetzold & All \\'+ '\n'
	myt += r'\hline'+'\n'

	for selector in selectors:
		selprefix = namem[selector]
		myt += selprefix + ' '
		for generator in generators:
			methodp = method[0].upper() + method[1:len(method)]
			data = results[generator][selector][method]
			comp = data[1]
			cstr = "%.3f" % comp
			if len(cstr)==1:
				cstr += '.000'
			elif len(cstr)==3:
				cstr += '00'
			elif len(cstr)==4:
				cstr += '0'
			myt += r'& $' + cstr + r'$ '
		myt += r'\\' + '\n'
		if selector in linebreakers:
			myt += r'\hline'+'\n'

	myt += r'\end{tabular}'+'\n'
	myt += r'\end{table}'+'\n'
	print(myt)
