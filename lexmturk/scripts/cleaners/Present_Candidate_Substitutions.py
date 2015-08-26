import os

generators = os.listdir('../../substitutions/')
generators = ['paetzold']

for generator in generators:
	print('Generator: ' + generator)
	try:
		file = '../../substitutions/'+generator+'/substitutions_void.txt'
		f = open(file)
		for line in f:
			data = line.strip().split('\t')

			sent = data[0]
			target = data[1]
			head = str(data[2])
			print('\tSentence: ' + sent)
			print('\tTarget: ' + target)
			print('\tHead: ' + head)

			print('\tCands:')
			cands = data[3:len(data)]
			for cand in cands:
				print('\t\t' + cand)		
		print('\n')
		f.close()
	except Exception:
		pass
