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
        config = map[type]['nn_mlp']
        config = config[0:len(config)-4].split('_')
	hidden = config[3]
	lr = config[4]
	momentum = config[5]
	decay = config[6]
	nesterov = config[7]
	layer = config[8]
	modelout = '../../../finalmodels/'+type+'/model_MLPBaselineFeatures_'+hidden+'_'+lr+'_'+momentum+'_'+decay+'_'+nesterov+'_'+layer
	comm = 'nohup python Train_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+modelout+' &'
	#comm = 'python Train_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+modelout
	os.system(comm)
