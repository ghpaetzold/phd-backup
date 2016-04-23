f = open('../../corpora/cwi_paetzold_training.txt')
o = open('../../corpora/cwi_paetzold_training_lower.txt', 'w')
for line in f:
	o.write(line.strip().lower() + '\n')
f.close()
o.close()

f = open('../../corpora/cwi_paetzold_testing.txt')
o = open('../../corpora/cwi_paetzold_testing_lower.txt', 'w')
for line in f:
        o.write(line.strip().lower() + '\n')
f.close()
o.close()
