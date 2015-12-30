import os

#Parameters:
hiddens = ['100']
layers = ['2', '5']
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_train.txt'
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_mlp')
	for hidden in hiddens:
		for layer in layers:
			output = '../../../labels/'+type+'/nn_mlp/labels_NeuralNetwork_MLP_'+hidden+'_'+layer+'.txt'
			modelout = '../../../models/'+type+'/model_MLPfeatures_'+hidden+'_'+layer
			comm = 'nohup python Run_NN_MLP.py '+trainset+' '+hidden+' '+layer+' '+testset+' '+output+' '+modelout+' &'
			os.system(comm)
