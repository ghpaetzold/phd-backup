import os

def getSuffix(file):
	path = file[0:len(file)-4]
	path = path.strip().split('_')
	return path[1].strip() + '_' + path[2].strip()

#Parameters:
losses = ['modified_huber', 'squared_hinge']
penalties = ['elasticnet']
alphas = ['0.1', '1']
l1_ratios = ['0.0', '0.5', '1.0']

#Get input files:
#trainfile = 'training_synonyms_antonyms.txt'
#testfile = 'testing_synonyms_antonyms.txt'
trainfile = 'training_synonymshypernyms_antonymshyponyms.txt'
testfile = 'testing_synonymshypernyms_antonymshyponyms.txt'
train = '../../corpora/datasets/'+trainfile
test = '../../corpora/datasets/'+testfile
suffix = getSuffix(train)
folder = 'sgd'

#Get models:
os.system('mkdir ../../classes/'+folder)
os.system('mkdir ../../classes/'+folder+'/'+suffix)

#Run classifiers:
tdfolder = '../../classes/'+folder+'/'+suffix
for loss in losses:
	for penalty in penalties:
		for alpha in alphas:
			for l1_ratio in l1_ratios:
				out = tdfolder + '/Loss=' + loss + '_Penalty=' + penalty + '_Alpha=' + alpha + '_L1Ratio=' + l1_ratio + '.txt'
				comm = 'nohup python SGD.py ' + loss + ' ' + penalty + ' ' + alpha + ' ' + l1_ratio + ' ' + train + ' ' + test + ' ' + out + ' &'
				print(comm)
				os.system(comm)
