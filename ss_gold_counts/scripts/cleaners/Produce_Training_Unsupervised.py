import os

def getSubs(generator):
        result = {}
        f = open('../../substitutions/' + generator + '/substitutions.txt')
        for line in f:
                data = line.strip().split('\t')
                target = data[0].strip()
                candidates = data[1].strip().split('|||')
                result[target] = candidates
        f.close()
	return result

generators = os.listdir('../../substitutions/')

for generator in generators:
	f = open('../../corpora/lexmturk_gold.txt')
	o = open('../../substitutions/'+generator+'/substitutions_unsupervised.txt', 'w')
	subs = getSubs(generator)
	for line in f:
		data = line.strip().split('\t')
		sent = data[0]
		target = data[1]
		head = int(data[2])
		
		newline = sent + '\t' + target + '\t' + str(head) + '\t1:' + target + '\t' 
		if target in subs:
			cands = subs[target]
			for cand in cands:
				if cand!=target:
					newline += '2:'+cand + '\t'
		o.write(newline.strip() + '\n')
	f.close()
	o.close()
	

