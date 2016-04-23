import os

#Parameters:
tasks = ['age', 'education', 'language', 'proficiency']
#tasks = ['age']
ks = ['2', '3', '4']
criterions = ['gini', 'entropy']
#criterions = ['gini']
splitters = ['best']
maxes = ['sqrt']
depths = ['None']

trainset = '../../corpora/cwi_training_multitask_decomposed.txt'
testset = '../../corpora/cwi_testing_multitask_decomposed.txt'
for task in tasks:
	os.system('mkdir ../../labels/'+task+'/decision')
	for c in criterions:
		for s in splitters:
			for m in maxes:
				for d in depths:
					for k in ks:
						output = '../../labels/'+task+'/decision/labels_DecisionTreeClassifier_'+c+'_'+s+'_'+m+'_'+d+'_'+k+'.txt'
						comm = 'nohup python Run_DecisionTree.py '+trainset+' '+k+' '+c+' '+s+' '+m+' '+d+' '+testset+' '+output+' '+task+' &'
						os.system(comm)
