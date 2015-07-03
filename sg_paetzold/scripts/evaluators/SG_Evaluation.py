from tabulate import tabulate
import os
from lexenstein.evaluators import *

def getData(model):
	d = model.split('_')
	amount = d[len(d)-1]
	ann = 'normal'
	if 'annotated' in model:
		ann = 'annotated'
	size = '500'
	if '300' in model:
		size = '300'

	arc = 'skip'
	if 'cbow' in model:
		arc = 'cbow'
	return ann, amount, arc, size

folder = '../../substitutions/'
files = os.listdir(folder)

metrics = ['Potential', 'Precision', 'Recall', 'F$1$']
anns = ['normal', 'annotated']
amounts = ['5', '10', '15', '20', '25']
arcs = ['cbow', 'skip']
sizes = ['300', '500']

resdata = {}
for m in metrics:
	resdata[m] = {}
	for an in anns:
		resdata[m][an] = {}
		for am in amounts:
			resdata[m][an][am] = {}
			for arc in arcs:
				resdata[m][an][am][arc] = {}
				for size in sizes:
					resdata[m][an][am][arc][size] = 0

for file in files:
	ann, amount, arc, size = getData(file)

	orig_p = folder+file
	
	orig_s = {}
	
	orig_f = open(orig_p)
	for line in orig_f:
		data = line.strip().split('\t')
		target = data[0].strip()
		if len(data)>1:
			subs = set(data[1].split('|||'))
			orig_s[target] = subs
	orig_f.close()
	
	ge = GeneratorEvaluator()
	pot, prec, rec, fmean = ge.evaluateGenerator('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt', orig_s)

	resdata['Potential'][ann][amount][arc][size] = "%.3f" % pot
	resdata['Precision'][ann][amount][arc][size] = "%.3f" % prec
	resdata['Recall'][ann][amount][arc][size] = "%.3f" % rec
	resdata['F$1$'][ann][amount][arc][size] = "%.3f" % fmean

counter = 0
for metric in metrics:
	for ann in anns:
		counter += 1
		table = r'\begin{table}[htpb]' + '\n'
		if ann=='annotated':
			table += r'\caption{' + metric + ' measures for word-sense aware embedding models}\n'
		else:
			table += r'\caption{' + metric + ' measures for traditional embedding models}\n'
		table += r'\centering' + '\n'
		table += r'\label{table:sgpaetzeval' + str(counter) + '}\n'
		table += r'\begin{tabular}{c|cc|cc}' + '\n'
		table += r' & \multicolumn{2}{c}{CBOW} & \multicolumn{2}{c}{Skip-Gram} \\' + '\n'
		table += r'\# & $300$ & $500$ & $300$ & $500$ \\' + '\n' + r'\hline' + '\n'
		for amount in amounts:
			table += r'$' + amount + r'$ & $' + str(resdata[metric][ann][amount]['cbow']['300']) + r'$ & '
			table += r'$' + str(resdata[metric][ann][amount]['cbow']['500']) + r'$ & '
			table += r'$' + str(resdata[metric][ann][amount]['skip']['300']) + r'$ & '
			table += r'$' + str(resdata[metric][ann][amount]['skip']['500']) + r'$ \\ ' + '\n'
		table += r'\end{tabular}' + '\n'
		table += r'\end{table}' + '\n\n'
		print(str(table))
