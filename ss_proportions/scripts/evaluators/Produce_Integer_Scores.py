import os
from lexenstein.evaluators import *

def getSelectors(generator):
	result = {}
	aux = {}

	files = os.listdir('../../substitutions/'+generator+'/')
	for file in files:
		if file != 'substitutions.txt' and 'unsupervised' not in file:
			filedata = file[0:len(file)-4].strip().split('_')
			bulk = filedata[1].strip()
			proportion = filedata[len(filedata)-1].strip()
			if '.' not in str(proportion):
				proportion = int(proportion)
				if bulk in result:
					aux[bulk][proportion] = 0.0
					if proportion in result[bulk]:
						result[bulk][proportion].add(file)
					else:
						result[bulk][proportion] = set([file])
				else:
					result[bulk] = {proportion: set([file])}
					aux[bulk] = {proportion: 0.0}
	return result, aux




#Selector name map:
namem = {}
namem['boundaryCV'] = 'Supervised Boundary Ranker'
namem['boundaryUnsupervisedCV'] = 'Unsupervised Boundary Ranker'
namem['svmranknotgt1st'] = 'Supervised SVM Ranker'
namem['subimdb22'] = 'Metric-Based Ranker'

#Generators:
generators = ['wordnet', 'kauchak', 'paetzold', 'all']

#Collect dataset data:
lexf = open('../../corpora/lexmturk_gold_test.txt')
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set([cand.split(':')[1].strip() for cand in data[3:len(data)]])
	lex.append((target, subs))
lexf.close()


#Create file containing best SS parameters:
for index in range(0, len(generators)):
	generator = generators[index]

	print(str(generator))
	out = open('../../integer_scores/'+generator+'.txt', 'w')

	selectors, result = getSelectors(generator)

	se = SelectorEvaluator()
	for selector in sorted(namem.keys()):
		newline = namem[selector] + '\t'

		print(str(sorted(selectors[selector])))
		for proportion in sorted(selectors[selector]):
			maxfmean = -1
			maxpot = -1
			maxprec = -1
			maxrec = -1
			maxfile = ''
			
			for file in selectors[selector][proportion]:

				#Generate sele_d (selected data):
				sele_d = []
				sele_p = '../../substitutions/'+generator+'/'+file	
	
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
						pot, prec, rec, fmean = se.evaluateSelector('../../corpora/lexmturk_gold_test.txt', sele_d)
						if fmean>maxfmean:
							maxfmean = fmean
							maxpot = pot
							maxprec = prec
							maxrec = rec
					except Exception:
						pass

			newline += str(maxpot)+'|||'+str(maxprec)+'|||'+str(maxrec)+'|||'+str(maxfmean)+'\t'
		out.write(newline.strip() + '\n')
	out.close()
