import os

#Parameters:
hiddens = ['100', '200']
layers = ['2', '3']
types = ['G', 'S', 'M', 'O']
embedsizes = ['100']
ngramsizes = ['2', '3']

for type in types:
	trainset = '../../../corpora/'+type+'_train.txt'
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_adadelta')
	for hidden in hiddens:
		for layer in layers:
			for embed in embedsizes:
				for ngram in ngramsizes:	
					output = '../../../labels/'+type+'/nn_adadelta/labels_NeuralNetwork_ADADELTA_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'.txt'
					modelout = '../../../models/'+type+'/model_ADADELTAallngrams_'+hidden+'_'+layer+'_'+embed+'_'+ngram
					comm = 'nohup python Run_NN_ADADELTA.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' &'
					os.system(comm)
