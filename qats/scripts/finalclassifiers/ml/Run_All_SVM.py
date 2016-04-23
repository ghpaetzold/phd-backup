import os

#Parameters:
Cs = ['1.0', '10.0']
kernels = ['rbf', 'linear']
ks = ['5', '10', 'all']
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_all.txt'
        testset = '../../../corpora/testset/'+type+'_all.txt'
        os.system('mkdir ../../../finallabels/'+type+'/svm')
	for C in Cs:
		for kernel in kernels:
			for k in ks:
				output = '../../../finallabels/'+type+'/svm/labels_SVM_'+C+'_'+kernel+'_'+k+'.txt'
				comm = 'nohup python Run_SVM.py '+trainset+' '+k+' '+' '+C+' '+kernel+' '+testset+' '+output+' &'
				os.system(comm)
