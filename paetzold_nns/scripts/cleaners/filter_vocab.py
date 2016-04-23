
def numberNotIn(word):
	numbers = '01234567890!?.-,'
	result = True
	for n in numbers:
		if n in word:
			result = False
	return result

f = open('../../corpora/vocab_rnnlm.txt')
o = open('../../corpora/vocab_rnnlm_20.txt', 'w')
c = 0
for line in f:
	c += 1
	print(str(c))
	data = line.split('\t')
	if len(data[0].strip())>0 and int(data[1].strip())>=20 and numberNotIn(data[0].strip()):
		o.write(line)
f.close()
o.close()
