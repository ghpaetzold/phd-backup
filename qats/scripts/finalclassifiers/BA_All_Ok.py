import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../finallabels/'+type+'/allok')
	f = open('../../corpora/testset/'+type+'_all.txt')
	o = open('../../finallabels/'+type+'/allok/allok.txt', 'w')
	for line in f:
		o.write('1\t1\n')
	f.close()
	o.close()

