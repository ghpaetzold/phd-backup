from tabulate import tabulate
import os
from lexenstein.evaluators import *

#generators = os.listdir('../../substitutions/')
generators = ['biran', 'wordnet', 'yamamoto', 'kauchak', 'paetzold']
selectors = ['first', 'random', 'path', 'lesk', 'clusters', 'biran']
#methods = set(os.listdir('../../rankings/'))
methods = ['length', 'colloc00', 'senses', 'synonyms', 'hypernyms', 'hyponyms']

namem = {}
namem['lesk'] = 'Lesk'
namem['first'] = 'First'
namem['random'] = 'Random'
namem['path'] = 'Wu-Palmer'
namem['clusters'] = 'Clusters'
namem['biran'] = 'Biran'
namem['void'] = 'No Selection'

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
	myt += namem[selector] + r' Selector}' + '\n'		
	myt += r'\centering'+'\n'
	myt += r'\label{table:w2vsgsssr'+str(index)+'}\n'
	myt += r'\begin{tabular}{l|cccccc}'+'\n'
	myt += r' & First & Random & Path & Lesk & Clusters & Biran \\'+ '\n'
	myt += r'\hline'+'\n'

	for generator in generators:
		genprefix = generator[0].upper() + generator[1:len(generator)]
		myt += genprefix + ' '
		for selector in selectors:
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
	myt += r'\end{tabular}'+'\n'
	myt += r'\end{table}'+'\n'
	print(myt)