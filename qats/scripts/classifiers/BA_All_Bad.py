import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../labels/'+type+'/allbad')
	f = open('../../corpora/'+type+'_test.txt')
	o = open('../../labels/'+type+'/allbad/allbad.txt', 'w')
	for line in f:
		o.write('0\t0\n')
	f.close()
	o.close()

