f = open('../../substitutions/all/substitutions.txt')
subs = {}
for line in f:
	data = line.strip().split('\t')
	word = data[0].strip()
	cands = set(data[1].strip().split('|||'))
	subs[word]=cands
f.close()

f = open('../../corpora/lexmturk_gold.txt')
o = open('../../corpora/lexmturk_nolabels.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	sent = data[0]
	target = data[1]
	head = data[2]
	cands = set([])
	if target in subs.keys():
		cands = subs[target]
	if target in cands:
		cands.remove(target)
	newline = sent + '\t' + target + '\t' + head + '\t1:' + target + '\t'
	for cand in cands:
		newline += '2:'+cand + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
