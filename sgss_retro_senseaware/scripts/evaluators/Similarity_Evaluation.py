import os
from tabulate import tabulate
from scipy.stats import *

#Parameters:
simfolder = '../../similarities/'
vector_size = '500'

#Datasets:
datasets = os.listdir(simfolder)

#Make one table for each dataset:
headers = ['Model-Arch', 'Spearman']
for dataset in datasets:
	print('\nDataset: ' + dataset)

	myt = []
	dpath = '../../corpora/wordsimilarity/'+dataset+'.txt'
	gold_similarities = [float(l.strip().split('\t')[2]) for l in open(dpath)]
	models = sorted(os.listdir(simfolder + dataset + '/'))

	for model in models:
		archs = sorted(os.listdir(simfolder + dataset + '/' + model + '/'))
		for arch in archs:
			try:
				name = model+'-'+arch.upper()
				pred_similarities = [float(l.strip()) for l in open(simfolder + dataset + '/' + model + '/' + arch + '/' + vector_size)]
				correlation = spearmanr(gold_similarities, pred_similarities)[0]
				myt.append([name, correlation])
			except Exception:
				pass
	print tabulate(myt, headers=headers)
