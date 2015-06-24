
f = open('../../corpora/lexmturk/lexmturk.txt')
o = open('../../corpora/lexmturk/lexmturk.new.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	if sent.startswith('\"'):
		sent = sent[1:len(sent)]
	if sent.endswith('\"'):
		sent = sent[0:len(sent)-1]
	target = data[1].strip()
	rest = data[2:len(data)]
	newline = sent + '\t' + target + '\t'
	for r in rest:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
