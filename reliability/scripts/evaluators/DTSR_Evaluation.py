from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Generators:
generators = os.listdir('../../substitutions/')
#generators = ['glavas']
#generators = ['paetzold']
#generators = ['kauchak']
#generators = ['biran']
generators = ['wordnet', 'kauchak', 'glavas', 'all']

#Selectors:
#selectors = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'nunes', 'wordvector', 'svmrank', 'boundaryUnsupervisedCV']
#selectors = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'GrammaticalityUS', 'MeaningUS', 'AppropriatenessUS']
selectors = ['void']

#Rankers:
datasets = os.listdir('../../dt_rankings/')
#methods = set(os.listdir('../../rankings/'))
#methods.remove('wiki00')

#Selector name map:
namem = {}
namem['lesk'] = 'Lesk'
namem['first'] = 'First'
namem['path'] = 'Path'
namem['biran'] = 'Biran'
namem['clusters'] = 'Belder'
namem['nunes'] = 'Nunes'
namem['svmrank'] = 'SVM Ranking'
#namem['boundaryUnsupervised'] = 'Unsupervised Boundary Ranking RAW'
namem['boundaryUnsupervisedCV'] = 'Unsupervised Boundary Ranking'
namem['wordvector'] = "Paetzold"
namem['void'] = 'Void'
namem['GrammaticalityUS'] = 'Grammaticality'
namem['MeaningUS'] = 'Meaning Preservation'
namem['AppropriatenessUS'] = 'Appropriateness'

#Generator name map:
genmap = {}
genmap['merriam'] = 'the Merriam generator'
genmap['yamamoto'] = 'the Yamamoto generator'
genmap['wordnet'] = 'the WordNet generator'
genmap['biran'] = 'the Biran generator'
genmap['kauchak'] = 'the Kauchak generator'
genmap['glavas'] = 'the Glavas generator'
genmap['paetzold'] = 'the Paetzold generator'
genmap['all'] = 'all generators combined'

#Ranker names:
srnamem = {}
srnamem['biran'] = 'Biran Ranker'
srnamem['bott'] = 'Bott Ranker'
srnamem['boundaryCV'] = 'Boundary Ranker'
srnamem['glavas'] = 'Glavas Ranker'
srnamem['kauchak'] = 'SVM Ranker'
srnamem['yamamoto'] = 'Yamamoto Ranker'
srnamem['brown00'] = 'Frequency: Brown'
srnamem['simplewiki00'] = 'Frequency'
srnamem['subimdb00'] = 'Frequency: SubIMDB'
srnamem['subtlex00'] = 'Frequency: SUBTLEX'
srnamem['senses'] = 'Senses'
srnamem['synonyms'] = 'Synonyms'
srnamem['hypernyms'] = 'Hypernyms'
srnamem['hyponyms'] = 'Hyponyms'
srnamem['length'] = 'Word Length'
srnamem['syllable'] = 'Syllable Count'

dtmap = {}
dtmap['semeval'] = 'SemEval'
dtmap['lexmturk'] = 'LexMTurk'
dtmap['debelder'] = 'LSeval'
dtmap['nnsimplex'] = 'NNSimpLex'

#Order:
#rankorder = ['length', 'syllable', 'senses', 'synonyms', 'hypernyms', 'hyponyms', 'simplewiki00', 'brown00', 'subtlex00', 'subimdb00']
#rankorder.extend(['biran', 'bott', 'yamamoto', 'kauchak', 'glavas', 'boundaryCV'])
#rankorder = ['simplewiki00', 'length', 'senses', 'synonyms', 'hypernyms', 'hyponyms']
rankorder = ['boundaryCV', 'kauchak']

results = {}
for generator in generators:
	results[generator] = {}
	for selector in selectors:
		results[generator][selector] = {}
		for dataset in datasets:
			results[generator][selector][dataset] = {}
			for method in rankorder:
				results[generator][selector][dataset][method] = (-1.0, -1.0, -1.0)

pe = PipelineEvaluator()
for dataset in datasets:
	methods = os.listdir('../../dt_rankings/'+dataset)
	for method in methods:
		#print(method)
		files = os.listdir('../../dt_rankings/'+dataset+'/'+method+'/')

		for file in files:
			filed = file.strip().split('.')[0].strip().split('_')
			generator = filed[1].strip()
			selector = filed[2].strip()

			subs = []
			f = open('../../dt_rankings/'+dataset+'/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			
			precision, accuracy, changed = pe.evaluatePipeline('../../corpora/paetzold_nns_dataset.txt', subs)
			
			try:
				if precision>results[generator][selector][dataset][method][2]:
					results[generator][selector][dataset][method] = (precision, accuracy, changed)
			except Exception:
				print('Problem: ' + str(file))
				pass

myt = ''
myt += r'\begin{table}[htpb]'+'\n'
#myt += r'\caption{Evaluation results for SR approaches with respect to substitutions generated by ' + genmap[generator]
myt += r'\caption{Round-trip scores with respect to substitutions generated by ' + genmap[generator]
myt += ', as selected by the '
myt += namem[selector] + r' Selector}' + '\n'
myt += r'\centering'+'\n'
myt += r'\label{table:srdatart}'+'\n'
myt += r'\begin{tabular}{l|l|cccccc}'+'\n'
myt += r' & & \multicolumn{2}{c}{Precision} & \multicolumn{2}{c}{Accuracy} & \multicolumn{2}{c}{Changed Proportion} \\'+ '\n'
myt += r'Generator & Dataset'
for i in range(0, 3):
	for method in rankorder:
		myt += r' & ' + method
myt += r' \\' + '\n'
myt += r'\hline'+'\n'

index = -1
for generator in results.keys():
	genprefix = generator[0].upper() + generator[1:len(generator)]
	for selector in selectors:
		index += 1
		for dataset in datasets:
			myt += generator + r' & ' + dtmap[dataset] + ' '
			for i in range(0, 3):
				for method in rankorder:
					data = [results[generator][selector][dataset][method][i]]
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
print(myt)
