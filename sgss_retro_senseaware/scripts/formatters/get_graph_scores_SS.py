import os
from lexenstein.evaluators import *

systems = ['TEM', 'REM', 'SEM', 'RSEM']
sizes = ['500', '700', '900', '1100', '1300', '1500', '1700', '1900', '2100', '2300', '2500']

o = open('../../corpora/selector_graph_scores.txt', 'w')

dataset = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

se = SelectorEvaluator()
for system in systems:
	newline = system + '\t'
	for size in sizes:
		sele_p = '../../selections/'+system+'/'+size
		sele_d = []
		sele_f = None
		sele_f = open(sele_p)
		for line in sele_f:
			data = line.strip().split('\t')
			data = data[3:len(data)]
			data = [candidate.strip().split(':')[1].strip() for candidate in data]
			if len(data)>0:
				sele_d.append(set(data))
			else:
				sele_d.append(set([]))
		sele_f.close()

		pot, prec, rec, fmean = se.evaluateSelector(dataset, sele_d)

		newline += str(pot)+'|||'+str(prec)+'|||'+str(rec)+'|||'+str(fmean) + '\t'
	o.write(newline.strip() + '\n')

o.close()
