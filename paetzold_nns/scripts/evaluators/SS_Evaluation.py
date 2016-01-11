import os
from lexenstein.evaluators import *

def getSelectors(map):
	result = {}
	files = os.listdir('../../substitutions/paetzold/')
	for file in files:
		if file != 'substitutions.txt':
			bulk = file[0:len(file)-4].strip().split('_')[1].strip()
			if bulk in result:
				result[bulk].add(file)
			else:
				result[bulk] = set([file])
	return result





#Selector name map:
namem = {}
namem['lesk'] = 'Lesk Algorithm'
#namem['lesk'] = 'Lesk'
namem['first'] = 'First Sense'
#namem['first'] = 'First'
#namem['random'] = 'Random'
#namem['wupalmer'] = 'Wu-Palmer'
namem['path'] = 'Path Similarity'
#namem['path'] = 'Path'
namem['biran'] = 'Biran Selector'
#namem['biran'] = 'Biran'
namem['clusters'] = 'Belder Selector'
#namem['clusters'] = 'Belder'
namem['aluisio'] = 'Aluisio Selector'
#namem['boundary'] = 'Boundary (No-CV)'
#namem['boundaryCV'] = 'Boundary (CV)'
namem['svmrank'] = 'SVM Ranking Selector'
namem['GrammaticalityUS'] = 'Grammaticality'
namem['MeaningUS'] = 'Meaning Preservation'
namem['AppropriatenessUS'] = 'Appropriateness'
namem['boundaryUnsupervisedCV'] = 'Unsupervised Boundary Selector'
#namem['boundaryUnsupervised'] = 'Boundary (Unsupervised)'
namem['wordvector'] = 'Paetzold Selector'
#namem['void'] = 'Void Selector'

#Selector order:
#selorder = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'nunes', 'wordvector', 'svmrank', 'boundaryUnsupervisedCV', 'GrammaticalityUS', 'MeaningUS', 'AppropriatenessUS']
selorder = ['void', 'first', 'lesk', 'path', 'biran', 'clusters', 'aluisio', 'wordvector', 'svmrank', 'boundaryUnsupervisedCV']

#Line breakers:
#breakers = set(['clusters'])
breakers = set([])

#Generator name map:
genmap = {}
genmap['merriam'] = 'the Merriam generator'
genmap['yamamoto'] = 'the Yamamoto generator'
genmap['wordnet'] = 'the Devlin generator'
genmap['biran'] = 'the Biran generator'
genmap['kauchak'] = 'the Kauchak generator'
genmap['glavas'] = 'the Glavas generator'
genmap['paetzold'] = 'the Paetzold generator'
genmap['all'] = 'all generators combined'

#Generators:
methods = os.listdir('../../substitutions/')
methods = ['merriam', 'yamamoto', 'wordnet', 'biran', 'kauchak', 'glavas', 'paetzold', 'all']
#methods = ['wordnet', 'kauchak', 'yamamoto', 'all']

#Dataset:
dataset = '../../corpora/paetzold_nns_dataset.txt'

#Create lex:
lexf = open(dataset)
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set([cand.split(':')[1].strip() for cand in data[3:len(data)]])
	lex.append((target, subs))
lexf.close()

#Selectors
selectors = getSelectors(namem)
maxims = selectors

#Create file containing best SS parameters:
topvs = [0.0,0.0,0.0,0.0]
topfs = ['','','','']
bestssf = open('best_ss.txt', 'w')
for index in range(0, len(methods)):
	method = methods[index]
	myt = ''
	headers = ['Selector', 'Potential', 'Precision', 'Recall', 'F1']
	myt += r'\begin{table}[htpb]'+'\n'
#	myt += r'\caption{Evaluation results for SS approaches with respect to substitutions generated by '+genmap[method]+'}\n'
	myt += r'\centering'+'\n'
#	myt += r'\label{table:benchss'+str(index)+'}\n'
#	myt += r'\label{table:uscwiss'+str(index)+'}\n'
	myt += r'\begin{tabular}{l|cccc}'+'\n'
	myt += r'Selector & Potential & Precision & Recall & F1 \\'+ '\n'
	myt += r'\hline'+'\n'

	se = SelectorEvaluator()
	for selector in selorder:
		if selector in maxims:
			maxfmean = -1
			maxpot = -1
			maxprec = -1
			maxrec = -1
			maxfile = ''
			for file in selectors[selector]:		
				#Generate sele_d (selected data):
				sele_d = []
				sele_p = '../../substitutions/'+method+'/'+file
	
				#index = -1
				sele_f = None
				try:
					sele_f = open(sele_p)
				except IOError:
					sele_f = None
				if sele_f:
					for line in sele_f:
						data = line.strip().split('\t')
						data = data[3:len(data)]
						data = [candidate.strip().split(':')[1].strip() for candidate in data]
					
						if len(data)>0:
							sele_d.append(set(data))
						else:
							sele_d.append(set([]))
					sele_f.close()
					
					try:
						pot, prec, rec, fmean = se.evaluateSelector(dataset, sele_d)
						if fmean>maxfmean:
#						if prec>maxprec:
							maxfmean = fmean
							maxpot = pot
							maxprec = prec
							maxrec = rec
							maxfile = file
					except Exception:
						print('Problem with: ' + selector)
						pass
			components = [maxpot, maxprec, maxrec, maxfmean]
			#print('For: ' + selector)
			#print('Max file: ' + maxfile)
			if selector in namem.keys():
				for k in range(0, len(components)):
					if components[k]>topvs[k]:
						topvs[k]=components[k]
						topfs[k]=method+'_'+selector
				if maxfmean>-1:
					bestssf.write(method + '\t' + selector + '\t' + maxfile.strip() + '\n')

				myt += namem[selector] + ' '
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
				if selector in breakers:
					myt += r'\hline' + '\n'
		else:
			for file in selectors[selector]:
				sele_d = []
				sele_p = '../../substitutions/'+method+'/'+file
				sele_f = None
				try:
					sele_f = open(sele_p)
				except IOError:
					sele_f = None
				if sele_f:
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
					components = [pot, prec, rec, fmean]
					identifier = file[0:len(file)-4].strip().split('_')
	
					if len(identifier)>2:
						identifier = identifier[2].strip()
						if identifier in namem.keys():
							bestssf.write(method + '\t' + identifier + '\t' + file.strip() + '\n')
							myt += namem[identifier] + ' '
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
	
	orig_p = '../../substitutions/'+method+'/substitutions.txt'
	orig_s = {}
	orig_d = []
	
	orig_f = open(orig_p)
	for line in orig_f:
		data = line.strip().split('\t')
		target = data[0].strip()
		if len(data)>1:
			subs = set(data[1].split('|||'))
			orig_s[target] = subs
	orig_f.close()
	
	#Generate orig_d (original data):
	for l in lex:
		target = l[0]
		if target in orig_s.keys():
			orig_d.append(orig_s[target])		
		else:
			orig_d.append(set([]))

	#Get statistics without selection:
	ge = GeneratorEvaluator()
	pot, prec, rec, fmean = ge.evaluateGenerator(dataset, orig_s)
	components = [pot, prec, rec, fmean]
	myt += r'\hline' + '\nNo Selection '
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
	myt += r'\caption{Evaluation results for SS approaches with respect to substitutions generated by '+genmap[method]+'}\n'
	myt += r'\label{table:benchss'+str(index)+'}\n'
	myt += r'\end{table}'+'\n'
	print(myt)
bestssf.close()

print('')
print('Top Potential: ' + str(topvs[0]) + ' - ' + topfs[0])
print('Top Precision: ' + str(topvs[1]) + ' - ' + topfs[1])
print('Top Recall: ' + str(topvs[2]) + ' - ' + topfs[2])
print('Top F1: ' + str(topvs[3]) + ' - ' + topfs[3])
