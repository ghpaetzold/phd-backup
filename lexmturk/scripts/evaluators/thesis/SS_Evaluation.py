import os
from lexenstein.evaluators import *

def getSelectors(map):
	result = {}
	files = os.listdir('../../../substitutions/kauchak/')
	for file in files:
		if file != 'substitutions.txt':
			bulk = file[0:len(file)-4].strip().split('_')[1].strip()
			if bulk in map:
				if bulk in result:
					result[bulk].add(file)
				else:
					result[bulk] = set([file])
	return result

#Generator names:
genmap = {}
genmap['biran'] = 'Biran'
genmap['kauchak'] = 'Kauchak'
genmap['merriam'] = 'Merriam'
genmap['wordnet'] = 'WordNet'
genmap['yamamoto'] = 'Yamamoto'
genmap['glavas'] = 'TEM'
genmap['glavasretrofitted'] = 'REM'
genmap['paetzold'] = 'SAEM'
genmap['paetzoldretrofitted'] = 'RSAEM'
genmap['all'] = 'All'

#Selector names:
namem = {}
namem['lesk'] = 'the Lesk Algorithm (Lesk)'
namem['first'] = 'the First Sense approach (First)'
namem['random'] = 'the Random Sense approach (Random)'
namem['path'] = 'the Path Similarity approach (Path)'
namem['biran'] = 'the Co-Occurrence Model Filtering approach (Biran)'
namem['clusters'] = 'the Word Clustering approach (Clusters)'

#Generators:
methods = ['biran', 'kauchak', 'wordnet', 'yamamoto', 'glavas', 'glavasretrofitted', 'paetzold', 'paetzoldretrofitted']
hlinemarker = 'glavas'

#Read data:
lexf = open('../../../corpora/lexmturk_all.txt')
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set([cand.split(':')[1].strip() for cand in data[3:len(data)]])
	lex.append((target, subs))
lexf.close()

#Selectors:
ss_map = getSelectors(namem)
selectors = ['random', 'first', 'lesk', 'path', 'clusters', 'biran']

#Create file containing best SS parameters:
bestssf = open('best_ss.txt', 'w')
for index in range(0, len(selectors)):
	selector = selectors[index]

	myt = ''
	myt += r'\begin{table}[htpb]'+'\n'
	myt += r'\caption{Results obtained by '+namem[selector]+'}\n'
	myt += r'\centering'+'\n'
	myt += r'\label{table:benchss'+str(index)+'}\n'
	myt += r'\begin{tabular}{l|cccc}'+'\n'
	myt += r'Selector & Potential & Precision & Recall & F-$1$ \\'+ '\n'
	myt += r'\hline'+'\n'

	se = SelectorEvaluator()
	for method in methods:
		maxfmean = -1
		maxpot = -1
		maxprec = -1
		maxrec = -1
		maxfile = ''
		for file in ss_map[selector]:		
			#Generate sele_d (selected data):
			sele_d = []
			sele_p = '../../../substitutions/'+method+'/'+file
	
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

				pot, prec, rec, fmean = se.evaluateSelector('../../../corpora/lexmturk_all.txt', sele_d)
				if fmean>maxfmean:
					maxfmean = fmean
					maxpot = pot
					maxprec = prec
					maxrec = rec
					maxfile = file
		components = [maxpot, maxprec, maxrec, maxfmean]
		if maxfmean>-1:
			bestssf.write(method + '\t' + selector + '\t' + maxfile.strip() + '\n')
		if method==hlinemarker:
			myt += r'\hline' + '\n'
		if selector in namem.keys():
			myt += genmap[method] + ' '
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
	if selector in namem.keys():
		print(myt)

bestssf.close()
