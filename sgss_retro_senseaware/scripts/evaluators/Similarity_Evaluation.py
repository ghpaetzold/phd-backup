import os
from tabulate import tabulate
from scipy.stats import *

#Parameters:
simfolder = '../../similarities/'
vector_size = '500'
archs = ['CBOW', 'SKIP']
models = ['TEM', 'REM', 'SEM', 'RSEM']

#Datasets:
datasets = os.listdir(simfolder)
datasets = ['MT-287', 'SCWS-2003', 'SIMLEX-999']

#Create map:
scoremap = {}
for model in models:
	scoremap[model] = {}
	for arch in archs:
		scoremap[model][arch] = {}
		for dataset in datasets:
			scoremap[model][arch][dataset] = 0.0

#Calculate scores:
myt = ''
myt += r'\begin{table}[htpb]'+'\n'
myt += r'\caption{Evaluation results for word similarity' + '}\n'
myt += r'\centering'+'\n'
myt += r'\label{table:wordsim}'+'\n'
myt += r'\begin{tabular}{l|ccc}'+'\n'
myt += r'Model & Arch.'
for dataset in datasets:
	myt += r' & ' + dataset
myt += r' \\' + '\n'
myt += r'\hline'+'\n'
for dataset in datasets:
	print('\nDataset: ' + dataset)

	#headers.append(dataset)
	dpath = '../../corpora/wordsimilarity/'+dataset+'.txt'
	gold_similarities = [float(l.strip().split('\t')[2]) for l in open(dpath)]
	#models = sorted(os.listdir(simfolder + dataset + '/'))

	for model in models:
		#archs = sorted(os.listdir(simfolder + dataset + '/' + model + '/'))
		for arch in archs:
			try:
				name = model+'-'+arch.upper()
				pred_similarities = [float(l.strip()) for l in open(simfolder + dataset + '/' + model + '/' + arch.lower() + '/' + vector_size)]
				scorrelation = spearmanr(gold_similarities, pred_similarities)[0]
				pcorrelation = pearsonr(gold_similarities, pred_similarities)[0]
				scoremap[model][arch][dataset] = scorrelation
				#myt.append([name, scorrelation, pcorrelation])
			except Exception:
				pass

for model in models:
	for arch in archs:
		vec = model + r' & ' + arch
		for dataset in datasets:
			comp = scoremap[model][arch][dataset]
			cstr = "%.3f" % comp
			if len(cstr)==1:
				cstr += '.000'
			elif len(cstr)==3:
				cstr += '00'
			elif len(cstr)==4:
				cstr += '0'
			vec += r' & $' + cstr +'$'
		vec += r' \\' + '\n'
		myt += vec
myt += r'\end{tabular}'+'\n'
myt += r'\end{table}'+'\n'
print myt
