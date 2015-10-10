import os

def getSuffix(file):
        path = file[0:len(file)-4]
        path = path.strip().split('_')
        return path[1].strip() + '_' + path[2].strip()

#Parameters:
Cs = ['10.0', '1.0']
kernels = ['rbf', 'sigmoid', 'linear']
degrees = ['2']
gammas = ['0.0', '1.0', '10.0']
coef0s = ['0.0', '1.0']

#Get input files:
trainfile = 'training_synonymshypernyms_antonymshyponyms.txt'
testfile = 'testing_synonymshypernyms_antonymshyponyms.txt'
train = '../../corpora/datasets/'+trainfile
test = '../../corpora/datasets/'+testfile
suffix = getSuffix(train)
folder = 'svm'

#Get models:
os.system('mkdir ../../classes/'+folder)
os.system('mkdir ../../classes/'+folder+'/'+suffix)
os.system('mkdir ../../models/'+folder)
os.system('mkdir ../../models/'+folder+'/'+suffix)

#Run classifiers:
tdfolder = '../../classes/'+folder+'/'+suffix
mdfolder = '../../models/'+folder+'/'+suffix
if 'rbf' in kernels:
	for C in Cs:
		for gamma in gammas:
			out = tdfolder + '/svc_rbf_C=' + C + '_Gamma=' + gamma + '.txt'
			model = mdfolder + '/svc_rbf_C=' + C + '_Gamma=' + gamma + '.txt'
			comm = 'nohup python SVM.py ' + C + ' rbf 1 ' + gamma + ' 0.0 ' + train + ' ' + test + ' ' + out + ' ' + model + ' &'
			print(comm)
			os.system(comm)
	
if 'sigmoid' in kernels:
        for C in Cs:
                for gamma in gammas:
                        for degree in degrees:
                                for coef0 in coef0s:
	                                        out = tdfolder + '/svc_sigmoid_C=' + C + '_Gamma=' + gamma + '_Coef0=' + coef0 + '.txt'
						model = mdfolder + '/svc_sigmoid_C=' + C + '_Gamma=' + gamma + '_Coef0=' + coef0 + '.txt'
	                                        comm = 'nohup python SVM.py ' + C + ' sigmoid 1 ' + gamma + ' ' + coef0 + ' ' + train + ' ' + test + ' ' + out + ' ' + model + ' &'
	                                        print(comm)
	                                        os.system(comm)
if 'linear' in kernels:
        for C in Cs:
		out = tdfolder + '/svc_linear_C=' + C + '.txt'
		model = mdfolder + '/svc_linear_C=' + C + '.txt'
		comm = 'nohup python SVM.py ' + C + ' linear 1 0.0 0.0 ' + train + ' ' + test + ' ' + out + ' ' + model + ' &'
		print(comm)
		os.system(comm) 
