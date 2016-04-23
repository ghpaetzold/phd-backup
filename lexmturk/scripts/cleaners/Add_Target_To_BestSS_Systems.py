import os

f = open('../evaluators/best_ss.txt')
for line in f:
	data = line.strip().split('\t')
	generator = data[0].strip()
	selector = data[1].strip()
	file = data[2].strip()
	if generator=='paetzold' and selector=='boundaryUnsupervisedCV':
		f = open('../../substitutions/'+generator+'/'+file)
		o = open('newfile.txt', 'w')
		for line in f:
			data = line.strip().split('\t')
			o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
		f.close()
		o.close()
		#os.system('mv newfile.txt oldfile.txt')
		os.system('mv newfile.txt ../../substitutions/'+generator+'/'+file)
f.close()
