f = open('../../substitutions/kauchak/substitutions_void.txt')
o = open('newfile.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
f.close()
o.close()
