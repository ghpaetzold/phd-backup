f = open('../../corpora/original.txt')
o1 = open('../../corpora/s1s.txt', 'w')
o2 = open('../../corpora/s2s.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	s1 = data[0].strip()
	s2 = data[1].strip()
	o1.write(s1+'\n')
	o2.write(s2+'\n')
f.close()
o1.close()
o2.close()