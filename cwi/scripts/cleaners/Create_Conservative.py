

f = open('../../corpora/cwi_training_allannotations.txt')
o = open('../../corpora/cwi_paetzold_training_conservative.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	labels = data[3:]
	c = 0
	for label in labels:
		if label=='1':
			c += 1
	final = '0'
	if c>=5:
		final = '1'
	o.write(data[0] + '\t' + data[1] + '\t' + data[2] + '\t' + final + '\n')
f.close()
o.close()
