import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../labels/'+type+'/allgood')
	f = open('../../corpora/'+type+'_test.txt')
	o = open('../../labels/'+type+'/allgood/allgood.txt', 'w')
	for line in f:
		o.write('2\t2\n')
	f.close()
	o.close()

