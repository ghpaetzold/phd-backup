from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../../rankings/')

#Names:
namem = {}
namem['biran'] = 'Biran Ranker'
namem['bott'] = 'Bott Ranker'
namem['paetzold'] = 'Boundary Ranker'
namem['glavas'] = 'Glavas Ranker'
namem['horn'] = 'SVM Ranker'
namem['WordLength'] = 'Word Length'
namem['NumberofSyllables'] = 'Number of Syllables'
namem['FrequencySubIMDB'] = 'Frequency: SubIMDB'
namem['FrequencySUBTLEX'] = 'Frequency: SUBTLEX'
namem['FrequencySimpleWiki'] = 'Frequency: SimpleWiki'
namem['FrequencyWikipedia'] = 'Frequency: Wikipedia'
namem['FrequencyBrown'] = 'Frequency: Brown'
namem['SenseCount'] = 'Sense Count'
namem['SynonymCount'] = 'Synonym Count'
namem['HypernymCount'] = 'Hypernym Count'
namem['HyponymCount'] = 'Hyponym Count'
namem['MinimumSenseDepth'] = 'Minimum Sense Depth'
namem['MaximumSenseDepth'] = 'Maximum Sense Depth'
namem['Ngramlef10right'] = r'N-gram $\left ( 1, 0 \right )$'
namem['Ngramlef01right'] = r'N-gram $\left ( 0, 1 \right )$'
namem['Ngramlef11right'] = r'N-gram $\left ( 1, 1 \right )$'
namem['Ngramlef20right'] = r'N-gram $\left ( 2, 0 \right )$'
namem['Ngramlef21right'] = r'N-gram $\left ( 2, 1 \right )$'
namem['Ngramlef02right'] = r'N-gram $\left ( 0, 2 \right )$'
namem['Ngramlef12right'] = r'N-gram $\left ( 1, 2 \right )$'
namem['Ngramlef22right'] = r'N-gram $\left ( 2, 2 \right )$'
namem['POSProb.'] = 'POS Prob.'
namem['TargetSim.'] = 'Target Sim.'
namem['ContextSim'] = 'Context Sim.'

#Order:
rankorder = []
rankorder.append(r'WordLength')
rankorder.append(r'NumberofSyllables')
rankorder.append(r'FrequencySubIMDB')
rankorder.append(r'FrequencySUBTLEX')
rankorder.append(r'FrequencySimpleWiki')
rankorder.append(r'FrequencyWikipedia')
rankorder.append(r'FrequencyBrown')
rankorder.append(r'SenseCount')
rankorder.append(r'SynonymCount')
rankorder.append(r'HypernymCount')
rankorder.append(r'HyponymCount')
rankorder.append(r'MinimumSenseDepth')
rankorder.append(r'MaximumSenseDepth')
rankorder.append(r'Ngramlef10right')
rankorder.append(r'Ngramlef01right')
rankorder.append(r'Ngramlef11right')
rankorder.append(r'Ngramlef20right')
rankorder.append(r'Ngramlef21right')
rankorder.append(r'Ngramlef02right')
rankorder.append(r'Ngramlef12right')
rankorder.append(r'Ngramlef22right')
rankorder.append(r'POSProb.')
rankorder.append(r'TargetSim.')
rankorder.append(r'ContextSim')
rankorder += ['biran', 'bott', 'horn', 'glavas', 'paetzold']

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

#for method in rankorder:
for method in rankorder:
	print('Method: ' + method)
	files = os.listdir('../../rankings/'+method+'/')
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
		f = open('../../rankings/'+method+'/'+file)
		for line in f:
			subs.append(line.strip().split('\t'))
		f.close()
			
		t1, t2, t3, r1, r2, r3 = re.evaluateRanker('../../corpora/NNSimpLex_test.txt', subs)
	
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
#	myt += method + ' '
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
