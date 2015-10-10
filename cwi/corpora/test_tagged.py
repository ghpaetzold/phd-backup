f = open('cwi_paetzold_training.txt')
t = open('tagged_sents_training_fixed.txt')
for line in f:
	data = line.strip().split('\t')
	sent1 = data[0].strip().split(' ')
	sent2 = t.readline().strip().split(' ')
	if len(sent1)!=len(sent2):
		print('Problem!')
f.close()
t.close()
