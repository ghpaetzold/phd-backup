f = open('../../substitutions/paetzold/substitutions_boundaryUnsupervisedCV_0.5_1_10_0.5_8nopos.txt')
o = open('newfile.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
f.close()
o.close()
