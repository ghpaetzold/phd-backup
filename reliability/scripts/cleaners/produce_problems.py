import os

rankers = os.listdir('../../rankings/')
rankers = ['subimdb00']
for ranker in rankers:
	print(ranker)
	files = os.listdir('../../rankings/'+ranker)
	for file in files:
		data = file.strip()
		data = data[0:len(data)-4].split('_')
		generator = data[1]
		selector = data[2]
		f1 = open('../../corpora/paetzold_nns_dataset.txt')
		f2 = open('../../rankings/'+ranker+'/'+file)
		o = open('../../problems/'+generator+'_'+selector+'_'+ranker+'.txt', 'w')
		for line in f1:
			data = line.strip().split('\t')
			sentence = data[0]
			target = data[1]
			head = data[2]
			candidates = f2.readline().strip().split('\t')
			candidate = target
			if len(candidates)>0:
				candidate = candidates[0]
			o.write(sentence + '\t' + target + '\t' + head + '\t0:' + target + '\t0:' + candidate + '\n')
		f1.close()
		f2.close()
		o.close()
			
