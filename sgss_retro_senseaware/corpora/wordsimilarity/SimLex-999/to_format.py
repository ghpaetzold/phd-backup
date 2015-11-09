f = open('SimLex-999.txt')
o = open('SimLex-999_fixed.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	word1 = data[0].strip()
	word2 = data[1].strip()
	sim = data[3].strip()
	o.write(word1 + '\t' + word2 + '\t' + sim + '\n')
f.close()
o.close()
