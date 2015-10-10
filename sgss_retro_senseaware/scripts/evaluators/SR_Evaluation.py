from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Names:
namem = {}
namem['boundary'] = 'Boundary Ranking'
namem['glavas'] = 'Glavas'
namem['svm'] = 'SVM'

#Order:
rankorder = ['boundary', 'glavas', 'svm']
types = ['TEM', 'SEM', 'REM', 'RSEM']
archs = ['cbow', 'skip']
size = '500'

#Initialize header:
myt = ''
myt += r'\begin{table}[htpb]'+'\n'
myt += r'\caption{Evaluation results for SR approaches' + '}\n'
myt += r'\centering'+'\n'
myt += r'\label{table:benchsr}'+'\n'
myt += r'\begin{tabular}{l|ccc}'+'\n'
myt += r'Ranker & TRank-at-1 & TRank-at-2 & TRank-at-3 \\'+ '\n'
myt += r'\hline'+'\n'

#Initialize evaluator:
re = RankerEvaluator()

for method in rankorder:
	for type in types:
		for arch in archs:
			maxt1 = -1
			maxt2 = -1
			maxt3 = -1
			maxf = ''
			c = 0
			files = os.listdir('../../solo_rankings/'+method+'/' + type + '/' + arch + '/' + size)
			for file in sorted(files):
				c += 1
				subs = []
				f = open('../../solo_rankings/'+method+'/' + type + '/' + arch + '/' + size+'/'+file)
				for line in f:
					subs.append(line.strip().split('\t'))
				f.close()
				t1, t2, t3, r1, r2, r3 = re.evaluateRanker('/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt', subs)
				if t1>maxt1:
					maxt1 = t1
					maxt2 = t2
					maxt3 = t3
					maxf = file
			print('Max: ' + str(t1))
			print('File: ' + maxf)
			print('\n')

			#Get statistics without selection:
			components = [maxt1, maxt2, maxt3]
			myt += namem[method] + '('+type+','+arch+') '
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
