import os

f = open('../evaluators/best_cwi.txt')
for line in f:
	data = line.strip().split('\t')
	system = data[0]
	file = data[1]
	comm = 'cp ../../labels/'+system+'/'+file+' ../../baselines/'+system+'.txt'
	os.system(comm)
f.close()
