import os
from lexenstein.evaluators import *

def getSelectors(map):
	result = {}
	files = os.listdir('../../substitutions/all/')
	for file in files:
		if file != 'substitutions.txt':
			bulk = file[0:len(file)-4].strip().split('_')[1].strip()
			if bulk in result:
				result[bulk].add(file)
			else:
				result[bulk] = set([file])
	return result




namem = {}
namem['DecisionTreeGrammaticality'] = 'Decision Trees (Grammaticality)'
namem['DecisionTreeBinGrammaticality'] = 'Decision Trees Bin (Grammaticality)'
namem['SGDClassifier'] = 'SGD Classifier (Grammaticality)'
namem['SVMClassifierGrammaticality'] = 'SVM Classifier (Grammaticality)'
namem['RandomTreesClassifierGrammaticality'] = 'Random Trees (Grammaticality'
namem['DecisionTreeJoint'] = 'Decision Trees (Joint)'
methods = ['biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto', 'all', 'paetzold']
methods = ['all']
lexf = open('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt')
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set([cand.split(':')[1].strip() for cand in data[3:len(data)]])
	lex.append((target, subs))
lexf.close()

selectors = getSelectors(namem)
maxims = set(selectors)

#Create file containing best SS parameters:
bestssf = open('best_ss.txt', 'w')
for index in range(0, len(methods)):
	method = methods[index]
	myt = ''
	headers = ['Selector', 'Potential', 'Precision', 'Recall', 'F-Measure']
	myt += r'\begin{table}[htpb]'+'\n'
	myt += r'\caption{Evaluation results for SS approaches with respect to substitutions generated by the '+method[0].upper()+method[1:len(method)]+' Generator}\n'
	myt += r'\centering'+'\n'
	myt += r'\label{table:benchss'+str(index)+'}\n'
	myt += r'\begin{tabular}{l|cccc}'+'\n'
	myt += r'Selector & Potential & Precision & Recall & F-Measure \\'+ '\n'
	myt += r'\hline'+'\n'

	se = SelectorEvaluator()
	for selector in sorted(selectors.keys()):
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
	
				index = -1
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
						pot, prec, rec, fmean = se.evaluateSelector('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', sele_d)
						if fmean>maxfmean:
							maxfmean = fmean
							maxpot = pot
							maxprec = prec
							maxrec = rec
							maxfile = file
					except Exception:
						pass
			components = [maxpot, maxprec, maxrec, maxfmean]
			#print('For: ' + selector)
			#print('Max file: ' + maxfile)
			if maxfmean>-1:
				bestssf.write(method + '\t' + selector + '\t' + maxfile.strip() + '\n')
			if selector in namem.keys():
				myt += namem[selector] + ' '
			else:
				myt += selector + ' '
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
						try:
							data = [candidate.strip().split(':')[1].strip() for candidate in data]
						except Exception:
							print(str(data))
						if len(data)>0:
							sele_d.append(set(data))
						else:
							sele_d.append(set([]))
					sele_f.close()
					
					try:
						pot, prec, rec, fmean = se.evaluateSelector('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', sele_d)
					except Exception:
						pot = 0.0
						prec = 0.0
						rec = 0.0
						fmean = 0.0
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
	pot, prec, rec, fmean = ge.evaluateGenerator('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', orig_s)
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
	myt += r'\end{table}'+'\n'
	print(myt)
bestssf.close()
