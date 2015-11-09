from tabulate import tabulate
import os
from lexenstein.evaluators import *

rankers = list(os.listdir('../../rankings/'))
generators = set([])
selectors = set([])
files = os.listdir('../../rankings/'+rankers[0])
for file in files:
	data = file[0:len(file)-4].split('_')
	generator = data[1]
	selector = data[2]
	generators.add(generator)
	selectors.add(selector)
methods = set(rankers)

results = {}
for generator in generators:
	results[generator] = {}
	for selector in selectors:
		results[generator][selector] = {}
		for method in methods:
			results[generator][selector][method] = (-1.0, -1.0, -1.0, 'None')

pe = PipelineEvaluator()
for method in methods:
		#print(method)
		files = os.listdir('../../rankings/'+method+'/')

		for file in files:
			filed = file.strip().split('.')[0].strip().split('_')
			print(file)
			generator = filed[1].strip()
			selector = filed[2].strip()

			subs = []
			f = open('../../rankings/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			
			try:
				precision, accuracy, changed = pe.evaluatePipeline('../../corpora/ls_dataset_benchmarking.txt', subs)
				
				try:
					if accuracy>results[generator][selector][method][0]:
						results[generator][selector][method] = (precision, accuracy, changed, file)
				except Exception:
					pass
			except Exception:
				pass

o = open('best_sr.txt', 'w')
for generator in results:
	for selector in results[generator]:
		for ranker in results[generator][selector]:
			newline = generator + '\t' + selector + '\t' + ranker + '\t' + results[generator][selector][ranker][3] + '\n'
			o.write(newline)
o.close()
