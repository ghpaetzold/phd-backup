import os

#Parameters:
ks = ['5', '10', 'all']
maxes = ['sqrt']
depths = ['4', '5', '6', '7', 'None']
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/dectrees')
	for m in maxes:
		for d in depths:
			for k in ks:
				output = '../../../labels/'+type+'/dectrees/labels_DecisionTrees_'+m+'_'+d+'_'+k+'.txt'
				comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+' '+m+' '+d+' '+testset+' '+output+' &'
				os.system(comm)
