#f = open('../../substitutions/kauchak/substitutions_void.txt')
f = open('../../substitutions/paetzold/substitutions_boundaryUnsupervisedCV_0.5_hinge_elasticnet_0.001_1.0_0.00001noCV.txt')
o = open('newfile.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
f.close()
o.close()
