import os
from lexenstein.evaluators import *

systems = ['glavas', 'glavas_retrofitted', 'paetzold', 'paetzold_retrofitted']
sizes = ['500', '700', '900', '1100', '1300', '1500', '1700', '1900', '2100', '2300', '2500']

o = open('../../corpora/generator_graph_scores.txt', 'w')

for system in systems:
	newline = system + '\t'
	for size in sizes:
		orig_p = '../../substitutions/'+system+size+'/substitutions.txt'

		orig_s = {}

		orig_f = open(orig_p)
		for line in orig_f:
			data = line.strip().split('\t')
			target = data[0].strip()
			if len(data)>1:
				subs = set(data[1].split('|||'))
				orig_s[target] = subs
		orig_f.close()
	
		ge = GeneratorEvaluator()
		pot, prec, rec, fmean = ge.evaluateGenerator('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', orig_s)

		newline += str(pot)+'|||'+str(prec)+'|||'+str(rec)+'|||'+str(fmean) + '\t'
	o.write(newline.strip() + '\n')

o.close()
