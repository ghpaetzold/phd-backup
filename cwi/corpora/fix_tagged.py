f = open('cwi_paetzold_training.txt')
t = open('tagged_sents_training.txt')

sentmap = {}
for line in t:
	data = line.strip().split(' ')
	sent = ''
	for token in data:
		tokend = token.strip().split('|||')
		word = tokend[0].strip()
		sent += word + ' '
	sentmap[sent.strip()] = line.strip()
t.close()

o = open('tagged_sents_training_fixed.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	o.write(sentmap[sent] + '\n')
o.close()
