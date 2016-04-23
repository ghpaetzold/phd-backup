from tabulate import tabulate
import os
from lexenstein.evaluators import *

#Generators:
generators = os.listdir('../../substitutions/')
#generators = ['glavas']
#generators = ['paetzold']
#generators = ['kauchak']
#generators = ['biran']
#generators = ['all']
generators.append('allvocab')
generators = ['allvocab']

#Selectors:
#selectors = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'aluisio', 'wordvector', 'svmrank', 'boundaryUnsupervisedCV']
#selectors = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'wordvector', 'boundaryUnsupervisedCV']
#selectors = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'GrammaticalityUS', 'MeaningUS', 'AppropriatenessUS']
#selectors = ['boundaryUnsupervisedCV']
selectors = ['void']
selectors = ['rnnlmlexmturk', 'rnnlmnnseval', 'rnnlmssuserstudy', 'rnnlmall']

#Rankers:
methods = set(os.listdir('../../rankings/'))
#methods.remove('wiki00')
methods = ['brown00', 'kauchak', 'glavas', 'rnnlmlexmturk', 'rnnlmnnseval', 'rnnlmssuserstudy', 'rnnlmall']
methods = ['brown00', 'kauchak', 'glavas']

#Selector name map:
namem = {}
namem['lesk'] = 'Lesk'
namem['first'] = 'First'
namem['path'] = 'Path'
namem['biran'] = 'Biran'
namem['clusters'] = 'Belder'
namem['aluisio'] = 'Aluisio'
namem['svmrank'] = 'SVM Ranking'
namem['boundaryUnsupervised'] = 'Unsupervised Boundary Ranking RAW'
namem['boundaryUnsupervisedCV'] = 'Unsupervised Boundary Ranking'
namem['wordvector'] = "Paetzold"
namem['void'] = 'Void'
namem['GrammaticalityUS'] = 'Grammaticality'
namem['MeaningUS'] = 'Meaning Preservation'
namem['AppropriatenessUS'] = 'Appropriateness'
namem['rnnlmall'] = 'NLM (All)'
namem['rnnlmlexmturk'] = 'NLM (LexMTurk)'
namem['rnnlmnnseval'] = 'NLM (NNSEval)'
namem['rnnlmssuserstudy'] = 'NLM (SSEval)'

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
genmap['allvocab'] = 'all words in the vocabulary'

#Ranker names:
srnamem = {}
srnamem['biran'] = 'Biran Ranker'
srnamem['bott'] = 'Bott Ranker'
srnamem['boundaryCV'] = 'Boundary Ranker'
srnamem['glavas'] = 'Glavas Ranker'
srnamem['kauchak'] = 'SVM Ranker'
srnamem['yamamoto'] = 'Yamamoto Ranker'
srnamem['brown00'] = 'Frequency: Brown'
srnamem['simplewiki00'] = 'Frequency: Simple Wiki'
srnamem['subimdb00'] = 'Frequency: SubIMDB'
srnamem['subtlex00'] = 'Frequency: SUBTLEX'
srnamem['brown22'] = 'N-gram: Brown'
srnamem['simplewiki22'] = 'N-gram: Simple Wiki'
srnamem['subimdb22'] = 'N-gram: SubIMDB'
srnamem['subtlex22'] = 'N-gram: SUBTLEX'
srnamem['senses'] = 'Senses'
srnamem['synonyms'] = 'Synonyms'
srnamem['hypernyms'] = 'Hypernyms'
srnamem['hyponyms'] = 'Hyponyms'
srnamem['length'] = 'Word Length'
srnamem['syllable'] = 'Syllable Count'
srnamem['rnnlmall'] = 'NLM (All)'
srnamem['rnnlmlexmturk'] = 'NLM (LexMTurk)'
srnamem['rnnlmnnseval'] = 'NLM (NNSEval)'
srnamem['rnnlmssuserstudy'] = 'NLM (SSEval)'

#Order:
rankorder = ['length', 'syllable', 'senses', 'synonyms', 'hypernyms', 'hyponyms', 'simplewiki00', 'brown00', 'subtlex00', 'subimdb00', 'simplewiki22', 'brown22', 'subtlex22', 'subimdb22']
rankorder.extend(['biran', 'bott', 'yamamoto', 'kauchak', 'glavas', 'boundaryCV'])
#rankorder = ['simplewiki00', 'length', 'senses', 'synonyms', 'hypernyms', 'hyponyms']
#rankorder = ['subimdb00']
#rankorder.extend(['subimdb10'])
#rankorder.extend(['subimdb01'])
#rankorder.extend(['subimdb11'])
#rankorder.extend(['subimdb02'])
#rankorder.extend(['subimdb12'])
#rankorder.extend(['subimdb20'])
#rankorder.extend(['subimdb21'])
#rankorder.extend(['subimdb22'])
#rankorder = ['glavas']
rankorder = ['brown00', 'kauchak', 'glavas', 'rnnlmlexmturk', 'rnnlmnnseval', 'rnnlmssuserstudy', 'rnnlmall']

results = {}
for generator in generators:
	results[generator] = {}
	for selector in selectors:
		results[generator][selector] = {}
		for method in rankorder:
#		for method in methods:
			results[generator][selector][method] = (-1.0, -1.0, -1.0)

pe = PipelineEvaluator()
for method in methods:
		#print(method)
		files = os.listdir('../../rankings/'+method+'/')

		maxfile = None
		for file in files:
			filed = file.strip().split('.')[0].strip().split('_')
			generator = filed[1].strip()
			selector = filed[2].strip()

			subs = []
			f = open('../../rankings/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			
			precision, accuracy, changed = pe.evaluatePipeline('../../corpora/paetzold_nns_dataset.txt', subs)
			
			try:
				if precision>results[generator][selector][method][0]:
					results[generator][selector][method] = (precision, accuracy, changed)
					if generator=='paetzold' and selector=='boundaryUnsupervisedCV' and method=='kauchak':
						maxfile = file
			except Exception:
				pass
#		if method=='kauchak':
#			print('File: ' + maxfile)
maxp = 0.0
maxpf = ''
maxa = 0.0
maxaf = ''
for generator in results:
	for selector in results[generator]:
		for ranker in results[generator][selector]:
			p = results[generator][selector][ranker][0]
			a = results[generator][selector][ranker][1]
			if p>maxp:
				maxp = p
				maxpf = generator+'_'+selector+'_'+ranker
			if a>maxa:
				maxa = a
				maxaf = generator+'_'+selector+'_'+ranker

print('Max Precision: ' + str(maxp) + ': ' + maxpf)
print('Max Accuracy: ' + str(maxa) + ': ' + maxaf)

index = -1
for generator in results.keys():
	genprefix = generator[0].upper() + generator[1:len(generator)]
	for selector in selectors:
		index += 1
		myt = ''
		myt += r'\begin{table}[htpb]'+'\n'
		#myt += r'\caption{Evaluation results for SR approaches with respect to substitutions generated by ' + genmap[generator]
		#myt += r'\caption{Round-trip scores with respect to substitutions generated by ' + genmap[generator]
		#myt += ', as selected by the '
		#myt += namem[selector] + r' Selector}' + '\n'		
		myt += r'\centering'+'\n'
		#myt += r'\label{table:benchsr'+str(index)+'}\n'
		#myt += r'\label{table:uscwirt'+str(index)+'}\n'
		myt += r'\begin{tabular}{l|ccc}'+'\n'
		myt += r'Ranker & Precision & Accuracy & Changed Proportion \\'+ '\n'
		myt += r'\hline'+'\n'
		for method in rankorder:
#		for method in methods:
			methodp = srnamem[method]
#			methodp = method
			myt += methodp + ' '
			data = results[generator][selector][method]
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
		myt += r'\caption{Round-trip scores with respect to substitutions generated by ' + genmap[generator]
		myt += ', as selected by the '
		myt += namem[selector] + r' Selector}' + '\n'
		myt += r'\label{table:benchpipe'+str(index)+'}\n'
		myt += r'\end{table}'+'\n'
		myt += r'\pagebreak'+'\n'
		print(myt)
