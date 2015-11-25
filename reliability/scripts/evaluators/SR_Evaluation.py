from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Systems:
systems = ['paetzold_boundaryUnsupervisedCV_subimdb00']

#Create map of deciders:
decidermap = {}
files = os.listdir('../../decisions')
for file in files:
	data = file[:len(file)-4].split('_')
	system = data[0]+'_'+data[1]+'_'+data[2]
	decider = data[3]
	if system not in decidermap:
		decidermap[system] = set([])
	decidermap[system].add(decider)


pe = PipelineEvaluator()
for system in systems:
	table = []
	for decider in sorted(list(decidermap[system])):
		subs = []
		f = open('../../decisions/'+system+'_'+decider+'.txt')
		for line in f:
			subs.append(line.strip().split('\t'))
		f.close()
		
		precision, accuracy, changed = pe.evaluatePipeline('../../corpora/paetzold_nns_dataset.txt', subs)
		f1 = 2*((precision*accuracy)/(precision+accuracy))
		
		table.append([decider, precision, accuracy, changed, f1])
	f = open('../../problems/'+system+'.txt')
	subs = []
	for line in f:
		data = line.strip().split('\t')
		target = data[1].strip()
		cands = set([word.strip().split(':')[1].strip() for word in data[3:]])
		cands.remove(target)
		subs.append([cands.pop()])
	precision, accuracy, changed = pe.evaluatePipeline('../../corpora/paetzold_nns_dataset.txt', subs)
	f1 = 2*((precision*accuracy)/(precision+accuracy))
	table.append(['No decision', precision, accuracy, changed, f1])
		
	print('For system: ' + system)
	print(tabulate(table))
