import os

methods = ['kauchak', 'biran', 'merriam', 'wordnet', 'yamamoto']

for method in methods:
	print(str(method))
	lexf = open('../../corpora/lexmturk/lexmturk.txt')
	subs = open('../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.txt')
	out = open('../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.clean.txt','w')

	csubs = 0
	cmiss = 0
	for line in subs:
		csubs += 1
		data = line.strip().split('\t')
		target = data[0].strip()
	
		linel = lexf.readline().strip()
		targetl = linel.split('\t')[1].strip()
	
		while targetl!=target:
			out.write(targetl + '\n')
			print('Trying to find ' + target)
			cmiss += 1
			linel = lexf.readline().strip()
			targetl = linel.split('\t')[1].strip()
		
		if len(data)>1:	
			out.write(target + '\t' + data[1].strip() + '\n')
		else:
			out.write(target + '\n')
	for line in lexf:
		targetl = line.split('\t')[1].strip()
		out.write(targetl + '\n')
	lexf.close()
	subs.close()
	out.close()
	
	print('Read: ' + str(csubs))
	print('Missed: ' + str(cmiss))
	os.system('rm ' + '../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.txt')
	os.system('mv ' + '../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.clean.txt ' + '../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.txt')
	os.system('rm ' + '../../corpora/substitutions/'+method+'/substitutions.enhanced_lesk.clean2.txt')
