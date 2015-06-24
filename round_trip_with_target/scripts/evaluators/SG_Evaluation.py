from tabulate import tabulate
import os
from lexenstein.evaluators import *

myt = []
headers = ['Method', 'Potential', 'Precision', 'Recall', 'F-Measure']

methods = ['biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto', 'all']

for method in methods:
	orig_p = '../../substitutions/'+method+'/substitutions.txt'
	
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
	pot, prec, rec, fmean = ge.evaluateGenerator('../../corpora/lexmturk_all.txt', orig_s)

	#Get statistics without selection:
	myt.append([method, "%.3f" % pot, "%.3f" % prec, "%.3f" % rec, "%.3f" % fmean])

print(tabulate(myt, headers, tablefmt="latex"))
