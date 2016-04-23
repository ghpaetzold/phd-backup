import os

#Packs of parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
	testset = '../../../corpora/'+type+'_test.txt'
	trainset = '../../../corpora/'+type+'_train.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_adadelta_final_adjusted')
	models = [m[0:len(m)-5].split('_')[2:] for m in os.listdir('../../../finalmodels/'+type) if m.endswith('.json')]
	print(str(models))
	for model in models:
		hidden = model[0]
		layer = model[1]
		embed = model[2]
		ngram = model[3]
		output = '../../../labels/'+type+'/nn_adadelta_final_adjusted/labels_NeuralNetwork_ADADELTAFINAL_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'.txt'
		modelout = '../../../finalmodels/'+type+'/model_ADADELTAallngrams_'+hidden+'_'+layer+'_'+embed+'_'+ngram
		comm = 'nohup python Predict_AdjustedInterval_Dev.py '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' '+trainset+' &'
		os.system(comm)
