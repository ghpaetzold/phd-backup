import os

files = sorted(os.listdir('../../corpora/text/split/'))

c = 0
for file in files:
	comm = 'nohup python3 Produce_Cooccur_Files.py ../../corpora/text/split/' + file + ' ../../corpora/cooccur_vectors/split/vecs.' + str(c) + '.txt &'
	print(comm)
	os.system(comm)
	c += 1


