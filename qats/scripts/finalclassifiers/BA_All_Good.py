import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../finallabels/'+type+'/allgood')
	f = open('../../corpora/testset/'+type+'_all.txt')
	o = open('../../finallabels/'+type+'/allgood/allgood.txt', 'w')
	for line in f:
		o.write('2\t2\n')
	f.close()
	o.close()

