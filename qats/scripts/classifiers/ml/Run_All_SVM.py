import os

#Parameters:
Cs = ['1.0', '10.0']
kernels = ['rbf', 'linear']
ks = ['5', '10', 'all']
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/svm')
	for C in Cs:
		for kernel in kernels:
			for k in ks:
				output = '../../../labels/'+type+'/svm/labels_SVM_'+C+'_'+kernel+'_'+k+'.txt'
				comm = 'nohup python Run_SVM.py '+trainset+' '+k+' '+' '+C+' '+kernel+' '+testset+' '+output+' &'
				os.system(comm)
