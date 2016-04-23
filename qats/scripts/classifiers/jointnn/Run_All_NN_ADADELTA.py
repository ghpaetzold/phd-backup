import os

#Parameters:
hiddens = ['100', '200']
layers = ['2', '3']
embedsizes = ['100']
ngramsizes = ['2', '3']

#trainset = '../../../corpora/'+type+'_train.txt'
#testset = '../../../corpora/'+type+'_test.txt'
#os.system('mkdir ../../../labels/'+type+'/nn_adadelta_joint')
for hidden in hiddens:
	for layer in layers:
		for embed in embedsizes:
			for ngram in ngramsizes:	
				modelout = '../../../models/JOINT/model_ADADELTAallngramsJoint_'+hidden+'_'+layer+'_'+embed+'_'+ngram
				comm = 'nohup python Run_NN_ADADELTA.py '+hidden+' '+layer+' '+embed+' '+ngram+' '+modelout+' &'
				#comm = 'python Run_NN_ADADELTA.py '+hidden+' '+layer+' '+embed+' '+ngram+' '+modelout
				os.system(comm)
