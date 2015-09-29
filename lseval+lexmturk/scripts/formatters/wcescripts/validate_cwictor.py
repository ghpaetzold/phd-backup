f = open('../../../corpora/wcefiles/cwictor_corpus_fixed.txt')
for line in f:
	data = line.strip().split('\t')
	if len(data)>3:
		sent = data[0].strip().split(' ')
		target = data[1].strip()
		head = int(data[2].strip())
		try:
			if sent[head]!=target:
				print('Problem: ' + str(line.strip()))
		except Exception:
			print('Exception: ' + str(line.strip()))
	else:
		print('Problem: ' + str(data))
f.close()
