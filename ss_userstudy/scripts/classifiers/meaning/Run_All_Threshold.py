import os

#Features: 21
flabels = []
flabels.append('colloc00')
flabels.append('colloc01')
flabels.append('colloc10')
flabels.append('colloc11')
flabels.append('postagprob')
flabels.append('transprob')
flabels.append('w2vpaetzold')
flabels.append('synonymy')
flabels.append('hypernymy')
flabels.append('hyponymy')

trainset = '../../../datasets/meaning_victor_training.txt'
testset = '../../../datasets/meaning_victor_testing.txt'
for i in range(0, len(flabels)):
	os.system('mkdir ../../../classes/meaning/' + flabels[i] + '/')
	output = '../../../classes/meaning/'+flabels[i]+'/labels_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Threshold.py '+trainset+' '+testset+' '+str(i)+' '+output+' &'
	os.system(comm)
