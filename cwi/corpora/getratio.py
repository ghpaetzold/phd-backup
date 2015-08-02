f = open('cwi_paetzold_training.txt')

complex = 0.0
all = 0.0
for line in f:
	data = line.strip().split('\t')
	label = data[3].strip()
	if label=='1':
		complex+=1.0
	all += 1.0
f.close()

print(str(complex/all))
