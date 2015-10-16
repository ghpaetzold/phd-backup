import os
from lexenstein.evaluators import *

systems = ['TEM', 'REM', 'SEM', 'RSEM']
sizes = ['500', '700', '900', '1100', '1300', '1500', '1700', '1900', '2100', '2300', '2500']

o = open('../../corpora/ranker_graph_scores.txt', 'w')

#Initialize evaluator:
re = RankerEvaluator()
for system in systems:
	newline = system + '\t'
	maxt1 = -1
	maxscores = []
	for size in sizes:
		files = os.listdir('../../solo_rankings/boundary/'+system+'/cbow/'+size)
		for file in files:
			subs = []
			f = open('../../solo_rankings/boundary/'+system+'/cbow/'+size+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
			t1, t2, t3, r1, r2, r3 = re.evaluateRanker('/export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt', subs)
			if t1>maxt1:
				maxt1 = t1
				maxscores = [t1, t2, t3]

		newline += str(maxscores[0])+'|||'+str(maxscores[1])+'|||'+str(maxscores[2]) + '\t'
	o.write(newline.strip() + '\n')

o.close()
