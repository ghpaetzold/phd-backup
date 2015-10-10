from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Initialize table:
myt = ''
myt += r'\begin{table}[htpb]'+'\n'
myt += r'\caption{Evaluation results for SG approaches' + '}\n'
myt += r'\centering'+'\n'
myt += r'\label{table:benchsg}'+'\n'
myt += r'\begin{tabular}{l|cccc}'+'\n'
myt += r'Generator & Potential & Precision & Recall & F1 \\'+ '\n'
myt += r'\hline'+'\n'

#Generators:
methods = sorted(os.listdir('../../substitutions/'))

#Name map:
genmap = {}
genmap['biran'] = 'Biran'
genmap['kauchak'] = 'Kauchak'
genmap['merriam'] = 'Merriam'
genmap['wordnet'] = 'WordNet'
genmap['yamamoto'] = 'Yamamoto'
genmap['glavas'] = 'Glavas'
genmap['paetzold'] = 'Paetzold'
genmap['all'] = 'All'

#Produce table:
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
	pot, prec, rec, fmean = ge.evaluateGenerator('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', orig_s)

	#Get statistics without selection:
	components = [pot, prec, rec, fmean]
	myt += method + ' '
	for comp in components:
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
