import os

#Parameters:
hiddens = ['100']
layers = ['2', '5']
types = ['G', 'S', 'M', 'O']
embeds = ['100', '300']
ngrams = ['2', '3']

for type in types:
	trainset = '../../../corpora/'+type+'_train.txt'
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_adam')
	for hidden in hiddens:
		for layer in layers:
			for embed in embeds:
				for ngram in ngrams:
					output = '../../../labels/'+type+'/nn_adam/labels_NeuralNetwork_Adam_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'.txt'
					modelout = '../../../models/'+type+'/model_ADAMallngrams_'+hidden+'_'+layer+'_'+embed+'_'+ngram
					comm = 'nohup python Run_NN_Adam.py '+trainset+' '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' &'
					os.system(comm)
