import os

#Packs of parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
	train_set = '../../../corpora/'+type+'_test.txt'
	os.system('mkdir ../../../labels/'+type+'/nn_mlp_final')
	models = [m[0:len(m)-5] for m in os.listdir('../../../finalmodels/'+type) if m.endswith('.json') and 'MLPBaselineFeatures' in m]
	print(str(models))
	for model in models:
		output = '../../../labels/'+type+'/nn_mlp_final/labels_NeuralNetwork_MLPFINAL_'+model[26:]+'.txt'
		modelout = '../../../finalmodels/'+type+'/'+model
		comm = 'nohup python Predict_Dev.py '+output+' '+modelout+' '+train_set+' &'
		os.system(comm)
