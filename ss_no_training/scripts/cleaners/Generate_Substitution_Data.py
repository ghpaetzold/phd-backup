subs = {}
f = open('../../substitutions/all/substitutions.txt')
for line in f:
	data = line.strip().split('\t')
	target = data[0].strip()
	cands = set(data[1].strip().split('|||'))
	subs[target] = cands
f.close()

f = open('../../corpora/lexmturk_gold.txt')
o = open('../../corpora/lexmturk_nosupervision.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	head = data[2].strip()
	cands = set([])
	if target in subs.keys():
		cands = subs[target]
	if target in cands:
		cands.remove(target)
	newline = sent + '\t' + target + '\t' + head + '\t1:' + target + '\t'

	myset = set([])
	for cand in cands:
		candata = cand.split(':')
		if candata[0] not in myset:
			myset.add(candata[0])
			newline += '2:' + candata[0] + '\t'
		else:
			print('lixo')
	o.write(newline.strip() + '\n')
f.close()
o.close()
