import os

#Parameters:
hiddens = ['20', '50']
losses = ['mean_squared_error', 'mean_absolute_error', 'binary_crossentropy']
optimizers = ['sgd', 'adagrad', 'adadelta', 'rmsprop', 'adam']

trainset = '../../../corpora/cwi_paetzold_training.txt'
testset = '../../../corpora/cwi_paetzold_testing.txt'
os.system('mkdir ../../../labels/nn')

for hidden in hiddens:
	for loss in losses:
		for optimizer in optimizers:
			output = '../../../labels/nn/labels_NeuralNetwork_'+hidden+'_'+loss+'_'+optimizer+'.txt'
			comm = 'nohup python Run_NN.py '+trainset+' '+hidden+' '+loss+' '+optimizer+' '+testset+' '+output+' &'
			os.system(comm)
