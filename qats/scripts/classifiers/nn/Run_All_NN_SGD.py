import os

#Parameters:
hiddens = ['100']
#hiddens = ['50']
layers = ['2', '3']
#layers = ['1']
types = ['G', 'S', 'M', 'O']
embedsizes = ['100']
ngramsizes = ['1', '2', '3']
archs = ['cbow']
retros = ['0']

for type in types:
	trainset = '../../../corpora/'+type+'_train.txt'
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_sgd')
	for hidden in hiddens:
		for layer in layers:
			for embed in embedsizes:
				for ngram in ngramsizes:
					for arch in archs:
						for retro in retros:
							output = '../../../labels/'+type+'/nn_sgd/labels_NeuralNetwork_SGD_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'_'+arch+'_'+retro+'.txt'
							modelout = '../../../models/'+type+'/model_SGDallngrams_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'_'+arch+'_'+retro
#							comm = 'python Run_NN_SGD.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' '+arch+' '+retro
							comm = 'nohup python Run_NN_SGD.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' '+arch+' '+retro+' &'
							os.system(comm)

