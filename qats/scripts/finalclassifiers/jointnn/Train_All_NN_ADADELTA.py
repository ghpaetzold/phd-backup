import os

types = ['G', 'S', 'M', 'O']

map = {}
for type in types:
	map[type] = {}

f = open('../../evaluators/best_accuracy.txt')
for line in f:
	data = line.strip().split('\t')
	type = data[0]
	system = data[1]
	file = data[2]
	map[type][system] = file
f.close()
print(str(map))

for type in types:
	trainset = '../../../corpora/'+type+'_all.txt'
	config = map[type]['nn_adadelta']
	config = config[0:len(config)-4].split('_')
	hidden = config[3]
	layer = config[4]
	embed = config[5]
	for ngram in ['2', '3']:
		modelout = '../../../finalmodels/'+type+'/model_ADADELTAallngrams_'+hidden+'_'+layer+'_'+embed+'_'+ngram
		comm = 'nohup python Train_NN_ADADELTA.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+modelout+' &'
		#comm = 'python Train_NN_ADADELTA.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+modelout
		os.system(comm)
