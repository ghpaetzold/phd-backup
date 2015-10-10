import os
from tabulate import tabulate
from scipy.stats import *

def getAccuracy(gold, pred):
	success = 0.0
	total = float(len(gold))
	for i in range(0, len(gold)):
		if gold[i]==pred[i]:
			success += 1.0
	return success/total

#Parameters:
simfolder = '../../toefl_answers/'
vector_size = '500'

#Make one table for each dataset:
headers = ['Model-Arch', 'Spearman']

myt = []
dpath = '../../corpora/toefl/toefl_testing.txt'
gold_answers = [l.strip() for l in open(dpath)]
models = sorted(os.listdir(simfolder))
for model in models:
	archs = sorted(os.listdir(simfolder + model + '/'))
	for arch in archs:
		name = model+'-'+arch.upper()
		pred_answers = [l.strip() for l in open(simfolder + model + '/' + arch + '/' + vector_size)]
		accuracy = getAccuracy(gold_answers, pred_answers)
		myt.append([name, accuracy])
print tabulate(myt, headers=headers)
