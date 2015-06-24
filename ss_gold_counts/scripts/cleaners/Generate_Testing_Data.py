

subs = {}
f = open('../../corpora/substitutions.txt')
for line in f:
	data = line.strip().split('\t')
	word = data[0].strip()
	cands = set(data[1].strip().split('|||'))
	subs[word] = cands
f.close()

r1 = open('../../corpora/substitutions_test.txt', 'w')
r2 = open('../../corpora/lexmturk_gold_counts.txt', 'w')
f = open('../../corpora/lexmturk_gold.txt')
gold_subs = {}
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	head = data[2].strip()
	candsd = set(data[3:len(data)])
	cands = set([])
	for cand in candsd:
		word = cand.strip().split(':')[1].strip()
		cands.add(word)
	
	r2.write(str(len(cands)) + '\n')

	substitutions = set([])
	if target in subs.keys():
		substitutions = subs[target]
	substitutions = substitutions.union(cands)
	
	if target not in gold_subs.keys():
		gold_subs[target] = substitutions
	else:
		gold_subs[target].update(substitutions)


for target in gold_subs.keys():
	substitutions = gold_subs[target]
	newline = target + '\t'
	for s in substitutions:
		newline += s + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]	

	r1.write(newline.strip() + '\n')
f.close()
r1.close()
r2.close()

