import os

gold = [line.strip().split('\t')[3] for line in open('../../corpora/cwi_gold_standard.txt')]

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

print('SG/SS...')
o = open('../../corpora/analysis/SGSS_non_cumulative.txt', 'w')
generators = os.listdir('../../substitutions/')
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
			ac = allcands[i]
			sc = simplecands[i]
			cs = cands[i]
			ainter = ac.intersection(cs)
			sinter = sc.intersection(cs)

			if gold[i]=='1':
				if len(ainter)==0:
					error3a += 1
				elif len(sinter)==0:
					error3b += 1
				else:
					noerror += 1
		o.write(generator + '\t' + selector + '\tOK='+str(noerror) + '\t3A='+str(error3a) + '\t3B='+str(error3b) + '\n')	
o.close()


print('SR...')
o = open('../../corpora/analysis/SR_non_cumulative.txt', 'w')
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
			ac = allcands[i]
			sc = simplecands[i]
			cs = cands[i]
			
			sub = ''
			if len(cs)>0:
				sub = cs[0]
			
			if gold[i]=='1':
				if sub not in ac:
					error4 += 1
				elif sub not in sc:
					error5 += 1
				else:
					noerror += 1
		o.write(generator + '\t' + selector + '\t' + ranker + '\tOK='+str(noerror) + '\t4='+str(error4) + '\t5='+str(error5) + '\n')
fr.close()
o.close()
