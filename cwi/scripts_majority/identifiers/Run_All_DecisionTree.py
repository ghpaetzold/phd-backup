import os

#Parameters:
ks = ['5', '6', '7']
#ks = ['9', '10', '11']
criterions = ['gini']
#criterions = ['entropy']
splitters = ['best']
maxes = ['sqrt']
depths = ['4', '5', '6', '7', '8', 'None']

trainset = '../../corpora/cwi_paetzold_training_majority.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					output = '../../labels_majority/decision/labels_DecisionTreeClassifier_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'.txt'
					comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
					os.system(comm)
