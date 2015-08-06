import os

#Parameters:
#ks = ['5', '6', '7', 'all']
ks = ['all']
#ks = ['all', '8', '7']
criterions = ['gini', 'entropy']
#criterions = ['gini']
splitters = ['best']
maxes = ['sqrt']
depths = ['4', '5', '6', '7', 'None']
#depths = ['None']

os.system('mkdir ../../../classes/meaning/decision/')

trainset = '../../../datasets/meaning_victor_training.txt'
testset = '../../../datasets/meaning_victor_testing.txt'
for c in criterions:
	for s in splitters:
		for m in maxes:
			for d in depths:
				for k in ks:
					output = '../../../classes/meaning/decision/labels_DecisionTreeClassifier_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'onlybin.txt'
					comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' &'
					print(comm)
					os.system(comm)
