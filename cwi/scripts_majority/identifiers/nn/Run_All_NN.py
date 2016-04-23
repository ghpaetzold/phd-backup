import os

#Parameters:
hiddens = ['100', '200', '300']
lrs = ['0.1']
momentums = ['0.01', '0.1']
decays = ['0.000001']
nesterovs = ['1']
layers = ['5', '6', '4']
#optimizers = ['sgd', 'adagrad', 'adadelta', 'rmsprop', 'adam']

trainset = '../../../corpora/cwi_paetzold_training_conservative.txt'
testset = '../../../corpora/cwi_paetzold_testing.txt'
os.system('mkdir ../../../labels_majority/nn')

for hidden in hiddens:
	for lr in lrs:
		for momentum in momentums:
			for decay in decays:
				for nesterov in nesterovs:
					for layer in layers:
						output = '../../../labels_majority/nn/labels_NeuralNetwork_SGD_'+hidden+'_'+lr+'_'+momentum+'_'+decay+'_'+nesterov+'_'+layer+'.txt'
						comm = 'nohup python Run_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+testset+' '+output+' &'
						#comm = 'python Run_NN.py '+trainset+' '+hidden+' '+lr+' '+momentum+' '+decay+' '+nesterov+' '+layer+' '+testset+' '+output
						os.system(comm)
