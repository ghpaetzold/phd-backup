import os

generators = os.listdir('../../substitutions/')
for generator in generators:
	f = open('../../substitutions/'+generator+'/substitutions_void.txt')
	o = open('newfile.txt', 'w')
	for line in f:
		data = line.strip().split('\t')
		o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
	f.close()
	o.close()
	os.system('mv newfile.txt ../../substitutions/'+generator+'/substitutions_void.txt')
f.close()
