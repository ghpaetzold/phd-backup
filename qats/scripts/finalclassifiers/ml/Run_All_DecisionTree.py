import os

#Parameters:
ks = ['5', '10', 'all']
maxes = ['sqrt']
depths = ['4', '5', '6', '7', 'None']
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_all.txt'
        testset = '../../../corpora/testset/'+type+'_all.txt'
        os.system('mkdir ../../../finallabels/'+type+'/dectrees')
	for m in maxes:
		for d in depths:
			for k in ks:
				output = '../../../finallabels/'+type+'/dectrees/labels_DecisionTrees_'+m+'_'+d+'_'+k+'.txt'
				comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+' '+m+' '+d+' '+testset+' '+output+' &'
				os.system(comm)
