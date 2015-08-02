import os
from lexenstein.evaluators import *

def getSelectors(map):
	result = {}
	files = os.listdir('../../../substitutions/kauchak/')
	for file in files:
		if file != 'substitutions.txt':
			bulk = file[0:len(file)-4].strip().split('_')[1].strip()
			if bulk in result:
				result[bulk].add(file)
			else:
				result[bulk] = set([file])
	return result


namem = {}
namem['lesk'] = 'Lesk'
namem['first'] = 'First'
namem['random'] = 'Random'
namem['path'] = 'Path'
namem['biran'] = 'Biran'
namem['clusters'] = 'Brown Clusters'
methods = ['biran', 'wordnet', 'yamamoto', 'kauchak', 'paetzold']
lexf = open('../../../corpora/lexmturk_all.txt')
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set([cand.split(':')[1].strip() for cand in data[3:len(data)]])
	lex.append((target, subs))
lexf.close()

ss_map = getSelectors(namem)
selectors = list(ss_map.keys())
maxims = set(['biran', 'clusters'])

#Create file containing best SS parameters:
bestssf = open('best_ss.txt', 'w')
for index in range(0, len(selectors)):
	selector = selectors[index]

	if selector in maxims:
		myt = ''
		myt += r'\begin{table}[htpb]'+'\n'
		myt += r'\caption{Results obtained by the '+selector+' SS approach}\n'
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
			if selector in namem.keys():
				myt += method[0].upper() + method[1:len(method)] + ' '
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
	else:
		se = SelectorEvaluator()
		for file in ss_map[selector]:
			identifier = file[0:len(file)-4].strip().split('_')
			if len(identifier)>2:
				identifier = identifier[2].strip()
			else:
				identifier = 'NULL'

			myt = ''
			myt += r'\begin{table}[htpb]'+'\n'
			myt += r'\caption{Results obtained by the '+identifier+' SS approach}\n'
			myt += r'\centering'+'\n'
			myt += r'\label{table:benchss'+str(index)+'}\n'
			myt += r'\begin{tabular}{l|cccc}'+'\n'
			myt += r'Selector & Potential & Precision & Recall & F-$1$ \\'+ '\n'
			myt += r'\hline'+'\n'	

			for method in methods:

				sele_d = []
				sele_p = '../../../substitutions/'+method+'/'+file
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
					components = [pot, prec, rec, fmean]

					if identifier in namem.keys():
						bestssf.write(method + '\t' + identifier + '\t' + file.strip() + '\n')
						myt += method[0].upper() + method[1:len(method)] + ' '
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
			if identifier in namem.keys():
				print(myt)
bestssf.close()
