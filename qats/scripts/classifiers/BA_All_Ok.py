import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../labels/'+type+'/allok')
	f = open('../../corpora/'+type+'_test.txt')
	o = open('../../labels/'+type+'/allok/allok.txt', 'w')
	for line in f:
		o.write('1\t1\n')
	f.close()
	o.close()

