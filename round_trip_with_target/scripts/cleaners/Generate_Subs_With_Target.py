

subs = {}
f = open('../../substitutions/kauchak/substitutions.txt')
for line in f:
	data = line.strip().split('\t')
	target = data[0].strip()
	cands = set(data[1].strip().split('|||'))
	subs[target] = cands
f.close()

f = open('../../../lexmturk/corpora/lexmturk_all.txt')
for line in f:
	data = line.strip().split('\t')
	target = data[1].strip()
	if target not in subs.keys():
		subs[target] = set([target])
	else:
		subs[target].add(target)
f.close()

f = open('../../substitutions/kauchak/substitutions_targets.txt', 'w')
for key in subs.keys():
	newline = key + '\t'
	for subst in subs[key]:
		newline += subst + '|||'
	newline = newline[0:len(newline)-3]
	f.write(newline.strip() + '\n')
f.close()
