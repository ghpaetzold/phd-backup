f = open('../../substitutions/kauchak/substitutions_void.txt')
o = open('newfile.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	target = data[1]
	cands = set([cand.strip().split(':')[1].strip() for cand in data[3:]])
	if target in cands:
		cands.remove(target)
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
