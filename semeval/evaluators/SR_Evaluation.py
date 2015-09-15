from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../rankings/')

#Names:
namem = {}
namem['biran'] = 'Biran Ranker'
namem['bott'] = 'Bott Ranker'
namem['paetzold'] = 'Boundary Ranker'
namem['glavas'] = 'Glavas Ranker'
namem['horn'] = 'SVM Ranker'
namem['yamamoto'] = 'Yamamoto Ranker'
namem['brown00'] = 'Frequency: Brown'
namem['simplewiki00'] = 'Frequency: Simple Wiki'
namem['subimdb00'] = 'Frequency: SubIMDB'
namem['subtlex00'] = 'Frequency: SUBTLEX'
namem['senses'] = 'Senses'
namem['synonyms'] = 'Synonyms'
namem['hypernyms'] = 'Hypernyms'
namem['hyponyms'] = 'Hyponyms'
namem['length'] = 'Word Length'
namem['syllable'] = 'Syllable Count'

#Order:
rankorder = ['length', 'syllable', 'senses', 'synonyms', 'hypernyms', 'hyponyms', 'simplewiki00', 'brown00', 'subtlex00', 'subimdb00']
rankorder.extend(['biran', 'bott', 'yamamoto', 'horn', 'glavas', 'paetzold'])

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
	print('Method: ' + method)
	files = os.listdir('../rankings/'+method+'/')
	maxt1 = -1
	maxt2 = -1
	maxt3 = -1
	maxr1 = -1
	maxr2 = -1
	maxr3 = -1
	maxf = ''
	c = 0
	for file in sorted(files):
		c += 1
		#print(str(c) + ' of ' + str(len(files)))
	
		subs = []
		f = open('../rankings/'+method+'/'+file)
		for line in f:
			subs.append(line.strip().split('\t'))
		f.close()
			
		t1, t2, t3, r1, r2, r3 = re.evaluateRanker('../corpora/semeval/semeval_test.txt', subs)
	
		if t1>maxt1:
			maxt1 = t1
			maxt2 = t2
			maxt3 = t3
			maxr1 = r1
			maxr2 = r2
			maxr3 = r3
			maxf = file
	print('Max: ' + str(t1))
	print('File: ' + maxf)
	print('\n')

	#Get statistics without selection:
	components = [maxt1, maxt2, maxt3]
	myt += namem[method] + ' '
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
