import sys, os, math, sys, numpy
from tabulate import tabulate

def getLabels(dataset):
	result = []
	f = open(dataset)
	for line in f:
		data = line.strip().split('\t')
		result.append(int(data[1]))
	return result

def getScores(hyp, ref):
	correct = 0
	for i in range(0, len(hyp)):
		if hyp[i] == ref[i]:
			correct += 1
	return float(correct)/float(len(hyp))

#Get main folder:
mainfolder = '../../classes/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get datasets:
datasets = os.listdir(mainfolder+mlfolders[0])

#Create total map:
totalmap = {}

for dataset in datasets:
	print('For test set: ' + dataset)

	table = []
	headers = ['Method', 'Accuracy', 'Model']

	#Get reference TER scores:
	ref = getLabels('../../corpora/datasets/testing_'+dataset+'.txt')
	
	#Get scores:
	for mlfolder in mlfolders:
		maxacc = 0.0
		maxfile = ''
		files = []
		try:
			files = os.listdir(mainfolder + mlfolder + '/' + dataset + '/')
		except Exception:
			pass
		for file in files:
			hyp = [int(x.strip()) for x in open(mainfolder + mlfolder + '/' + dataset + '/' + file)]
			if len(ref)==len(hyp):
				acc = getScores(hyp, ref)
				if acc>maxacc:
					maxacc = acc
					maxfile = file
		table.append([mlfolder, "%.3f" % maxacc, maxfile])
	print(tabulate(table, headers=headers) + '\n')
