import os

#Packs of parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
	testset = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_adadelta_regression_final')
	models = [m[0:len(m)-5].split('_')[2:] for m in os.listdir('../../../finalmodels/'+type) if m.endswith('.json') and 'ADADELTARegression' in m]
	print(str(models))
	for model in models:
		hidden = model[0]
		layer = model[1]
		embed = model[2]
		ngram = model[3]
		output = '../../../labels/'+type+'/nn_adadelta_regression_final/labels_NeuralNetwork_ADADELTAFINALRegression_'+hidden+'_'+layer+'_'+embed+'_'+ngram+'.txt'
		modelout = '../../../finalmodels/'+type+'/model_ADADELTARegression_'+hidden+'_'+layer+'_'+embed+'_'+ngram
		comm = 'nohup python Predict_Dev.py '+hidden+' '+layer+' '+embed+' '+ngram+' '+testset+' '+output+' '+modelout+' &'
		os.system(comm)
