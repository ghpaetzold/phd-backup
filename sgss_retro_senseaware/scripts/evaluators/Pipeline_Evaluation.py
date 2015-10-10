from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Models:
models = ['TEM', 'REM', 'SEM', 'RSEM']

#Map:
map = {}
for model in models:
	map[model] = (0.0, 0.0, 0.0)

pe = PipelineEvaluator()
for model in models:
		files = os.listdir('../../rankings/boundary/'+model+'/')

		for file in files:
			subs = []
			f = open('../../rankings/boundary/'+model+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			
			precision, accuracy, changed = pe.evaluatePipeline('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', subs)
			
			try:
				if precision>map[model][1]:
					map[model] = (precision, accuracy, changed)
			except Exception:
				pass

myt = ''
myt += r'\begin{table}[htpb]'+'\n'
#myt += r'\caption{Evaluation results for SR approaches with respect to substitutions generated by ' + genmap[generator]
myt += r'\caption{Round-trip scores}\n'		
myt += r'\centering'+'\n'
#myt += r'\label{table:benchsr'+str(index)+'}\n'
myt += r'\label{table:roundtriprsem}\n'
myt += r'\begin{tabular}{l|ccc}'+'\n'
myt += r'Ranker & Precision & Accuracy & Changed Proportion \\'+ '\n'
myt += r'\hline'+'\n'
for model in models:
	methodp = model
	myt += methodp + ' '
	data = map[model]
	for comp in data:
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
myt += r'\pagebreak'+'\n'
print(myt)