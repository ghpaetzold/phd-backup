import os

#Parameters:
hiddens = ['100', '200']
#hiddens = ['100']
lrs = ['0.1']
momentums = ['0.01', '0.1']
#momentums = ['0.01']
decays = ['0.000001']
nesterovs = ['1']
layers = ['1', '2', '3']
#layers = ['1']
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_train.txt'
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_mlp')
	for hidden in hiddens:
		for lr in lrs:
			for momentum in momentums:
				for decay in decays:
					for nesterov in nesterovs:
						for layer in layers:
							output = '../../../labels/'+type+'/nn_mlp/labels_NeuralNetwork_MLP_'+hidden+'_'+lr+'_'+momentum+'_'+decay+'_'+nesterov+'_'+layer+'.txt'
							modelout = '../../../models/'+type+'/model_MLPBaselineFeatures_'+hidden+'_'+lr+'_'+momentum+'_'+decay+'_'+nesterov+'_'+layer
							comm = 'nohup python Run_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+testset+' '+output+' '+modelout+' &'
							#comm = 'python Run_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+testset+' '+output+' '+modelout
							os.system(comm)
