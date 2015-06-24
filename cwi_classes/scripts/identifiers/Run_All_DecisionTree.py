import os

#Parameters:
ks = ['5', '6', '7', '10']
#ks = ['2', '3', '4', '8', '9']
criterions = ['gini', 'entropy']
splitters = ['best']
maxes = ['sqrt']
depths = ['4', '5', '6', '7', 'None']

trainset = '../../corpora/cwi_paetzold_training'
testset = '../../corpora/cwi_paetzold_testing'
for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					output = '../../labels/decision/labels_DecisionTreeClassifier_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'_w2v.txt'
					comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
					os.system(comm)
