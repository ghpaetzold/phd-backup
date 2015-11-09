import os

#Parameters:
sizes = ['700', '900', '1100']
archs = ['skip']
#archs = ['cbow']

for arch in archs:
	for size in sizes:
		comm = 'nohup python Run_Metric.py /export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt '
		comm += size + ' ' + arch + ' &'
		os.system(comm)
