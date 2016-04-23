import os

types = ['G', 'M', 'S', 'O']

for type in types:
	os.system('mkdir ../../finallabels/'+type+'/allbad')
	f = open('../../corpora/testset/'+type+'_all.txt')
	o = open('../../finallabels/'+type+'/allbad/allbad.txt', 'w')
	for line in f:
		o.write('0\t0\n')
	f.close()
	o.close()

