import os

generators = os.listdir('../../substitutions/')

for generator in generators:
	try:
		file = '../../substitutions/'+generator+'/substitutions_void.txt'
		avg = 0
		f = open(file)
		for line in f:
			data = line.strip().split('\t')
			cands = data[3:len(data)]
			avg += len(cands)	
		f.close()
		print('Generator: ' + generator + ', candidates: ' + str(float(avg)/500.0))
	except Exception:
		pass
