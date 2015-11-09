import os

gold = [line.strip().split('\t')[3] for line in open('../../corpora/cwi_gold_standard.txt')]

f = open('../evaluators/best_cwi.txt')
methodmap = {}
for line in f:
	data = line.strip().split('\t')
	method = data[0].strip()
	file = data[1].strip()
	methodmap[method] = file
f.close()

#Generate statistics for CWI systems:
print('CWI...')
o = open('../../corpora/analysis/CWI.txt', 'w')
for method in sorted(methodmap.keys()):
	pred = [line.strip() for line in open('../../labels/'+method+'/'+methodmap[method])]
	methodmap[method] = pred
	noerror = 0
	error2a = 0
	error2b = 0
	for i in range(0, len(gold)):
		g = gold[i]
		p = pred[i]
		if p=='0' and g=='0':
			noerror += 1
		elif p=='0' and g=='1':
			error2a += 1
		elif p=='1' and g=='0':
			error2b += 1
		else:
			noerror += 1
	o.write(method + '\tOK='+str(noerror) + '\t2A='+str(error2a) + '\t2B='+str(error2b) + '\n')
o.close()
print('')

#Get generation/selection errors:
selfilemap = {}
f = open('../evaluators/best_ss.txt')
for line in f:
	data = line.strip().split('\t')
	gen = data[0].strip()
	sel = data[1].strip()
	file = data[2].strip()
	if gen not in selfilemap:
		selfilemap[gen] = {}
	selfilemap[gen][sel] = file
f.close()

allcands = []
simplecands = []
f = open('../../corpora/ls_dataset_benchmarking.txt')
for line in f:
	data = line.strip().split('\t')
	cs = set([cand.strip().split(':')[1].strip() for cand in data[3:]])
	allcands.append(cs)
f.close()
f = open('../../corpora/ls_dataset_benchmarking_simple.txt')
for line in f:
        data = line.strip().split('\t')
        cs = set([cand.strip().split(':')[1].strip() for cand in data[3:]])
        simplecands.append(cs)
f.close()
print(str(simplecands))

print('SG/SS...')
o = open('../../corpora/analysis/SGSS.txt', 'w')
generators = os.listdir('../../substitutions/')
for identifier in methodmap:
	print(identifier)
	for generator in selfilemap:
		for selector in selfilemap[generator]:
			f = open('../../substitutions/'+generator+'/'+selfilemap[generator][selector])
			cands = []
			for line in f:
				data = line.strip().split('\t')
				cs = set([cand.strip().split(':')[1].strip() for cand in data[3:]])
				cands.append(cs)
			f.close()
		
			noerror = 0
			error3a = 0
			error3b = 0
			for i in range(0, len(allcands)):
				gold_label = gold[i]
				pred_label = methodmap[identifier][i]
				ac = allcands[i]
				sc = simplecands[i]
				cs = cands[i]
				if gold_label=='0':
					sc = set([])
				else:
					if pred_label=='0':
						cs = set([])		
				ainter = ac.intersection(cs)
				sinter = sc.intersection(cs)
	
				if gold_label=='1':
					if len(ainter)==0:
						error3a += 1
					elif len(sinter)==0:
						error3b += 1
					else:
						noerror += 1
			o.write(identifier + '\t' + generator + '\t' + selector + '\tOK='+str(noerror) + '\t3A='+str(error3a) + '\t3B='+str(error3b) + '\n')	
o.close()
	

print('SR...')
o = open('../../corpora/analysis/SR.txt', 'w')
for identifier in methodmap:
	fr = open('../evaluators/best_sr.txt')
	for line in fr:
		frdata = line.strip().split('\t')
		generator = frdata[0]
		selector = frdata[1]
		ranker = frdata[2]
		file = frdata[3]

		f = open('../../rankings/'+ranker+'/'+file)
		cands = []
		for line in f:
			data = line.strip().split('\t')
			cands.append(data)
		f.close()

		if len(cands)!=929:
			print('File: ' + '../../rankings/'+ranker+'/'+file)
		else:
			error4 = 0
			error5 = 0
			noerror = 0
			for i in range(0, len(allcands)):
				gold_label = gold[i]
				pred_label = methodmap[identifier][i]
				ac = allcands[i]
				sc = simplecands[i]
				cs = cands[i]
				if gold_label=='0':
					sc = set([])
				else:
					if pred_label=='0':
						cs = set([])
				
				sub = ''
				if len(cs)>0:
					sub = cs[0]
				
				if sub not in ac:
					error4 += 1
				elif sub not in sc:
					error5 += 1
				else:
					noerror += 1
			o.write(identifier + '\t' + generator + '\t' + selector + '\t' + ranker + '\tOK='+str(noerror) + '\t4='+str(error4) + '\t5='+str(error5) + '\n')
	fr.close()
o.close()
