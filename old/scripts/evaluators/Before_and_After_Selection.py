import os

def getStatistics(lex, data):
	potential = 0.0
	noise = 0.0
	fmean = 0.0
	noised = 0.0

	for i in range(0, len(lex)):
		l = lex[i]
		d = data[i]
		
		over = l[1].intersection(d)
		if len(over)>0:
			potential += 1

		if len(d)>0:
			#noise += float(len(over))/float(len(d))
			noise += float(len(over))
			noised += float(len(d))

	potential /= float(len(lex))
	#noise /= float(len(lex))
	noise = noise/noised

	if potential==0.0 and noise==0.0:
		fmean = 0.0
	else:
		fmean = 2*(potential*noise)/(potential+noise)

	return potential, noise, fmean

def getSelectors():
	files = os.listdir('../../corpora/substitutions/kauchak/')
	result = set([])
	for file in files:
		if file.startswith('substitutions'):
			data = file.strip().split('.')
			if len(data)>2:
				result.add(data[1].strip())
	return sorted(list(result))
















methods = ['biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto', 'all']

lexf = open('../../corpora/lexmturk/lexmturk.txt')
lex = []
for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	subs = set(data[2:len(data)])
	lex.append((target, subs))
lexf.close()

selectors = getSelectors()

final_results = {}

for method in methods:
	final_results[method] = {}

	orig_p = '../../corpora/substitutions/'+method+'/substitutions.txt'
	
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
	orig_pot, orig_noise, orig_fmean = getStatistics(lex, orig_d)
	final_results[method]['no_selection'] = (orig_pot, orig_noise, orig_fmean)

	for selector in selectors:		
		#Generate sele_d (selected data):
		sele_d = []
		sele_p = '../../corpora/substitutions/'+method+'/substitutions.'+selector+'.txt'

		index = -1
		sele_f = open(sele_p)
		for line in sele_f:
			data = line.strip().split('\t')
			target = data[0].strip()	
		
			index += 1
			targetl = lex[index][0]
			while targetl!=target:
				index += 1
				targetl = lex[index][0]
				sele_d.append(set([]))
			
			if len(data)>1:
				sele_d.append(set(data[1].strip().split('|||')))
			else:
				sele_d.append(set([]))
		sele_f.close()			
	
		for i in range(index+1, 500):
			sele_d.append(set([]))

		sele_pot, sele_noise, sele_fmean = getStatistics(lex, sele_d)

		final_results[method][selector] = (sele_pot, sele_noise, sele_fmean)	

for m in final_results.keys():
	print('Method ' + m + ':')
	for s in sorted(list(final_results[m].keys())):
		data = final_results[m][s]
		print('\t' + s + ':\t' + str(data[0]) + '\t' + str(data[1]) + '\t' + str(data[2]))
