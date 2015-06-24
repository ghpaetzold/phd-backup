from tabulate import tabulate
import os
from lexenstein.evaluators import *

methods = os.listdir('../rankings/')

maxes = set(['svm_original', 'boundary', 'bott', 'biran', 'yamamoto', 'paetzold', 'horn', 'svm_top1', 'svm_top2', 'svm_top2e', 'svm_top3', 'paetzoldCV', 'paetzoldpop'])
alls = set(['metrics'])

re = RankerEvaluator()

myt = []
#headers = ['Method', 'TRank-at-1', 'TRank-at-2', 'TRank-at-3', 'Recall-at-1', 'Recall-at-2', 'Recall-at-3']
headers = ['Method', 'TRank', 'Recall-at-1', 'Recall-at-2', 'Recall-at-3']
for method in methods:
	if method in maxes:
		print('Method: ' + method)
		files = os.listdir('../rankings/'+method+'/')
		maxt1 = -1
		maxt2 = -1
		maxt3 = -1
		maxr1 = -1
		maxr2 = -1
		maxr3 = -1
		maxf = ''
		c = 0
		for file in sorted(files):
			c += 1
			#print(str(c) + ' of ' + str(len(files)))
		
			subs = []
			f = open('../rankings/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()
				
			t1, t2, t3, r1, r2, r3 = re.evaluateRanker('../corpora/semeval/semeval_test.txt', subs)
		
			if t1>maxt1:
				maxt1 = t1
				maxt2 = t2
				maxt3 = t3
				maxr1 = r1
				maxr2 = r2
				maxr3 = r3
				maxf = file
		
		print('Max t1: ' + str(maxt1))
		print('Max t2: ' + str(maxt2))
		print('Max t3: ' + str(maxt3))
		print('Max file: ' + maxf)
		#myt.append([method[0].upper()+method[1:len(method)],'$'+"%.3f" % maxt1+'$', '$'+"%.3f" % maxt2+'$', '$'+"%.3f" % maxt3+'$', '$'+"%.3f" % maxr1+'$', '$'+"%.3f" % maxr2+'$', '$'+"%.3f" % maxr3+'$'])
		myt.append([method[0].upper()+method[1:len(method)],'$'+"%.3f" % maxt1+'$', '$'+"%.3f" % maxr1+'$', '$'+"%.3f" % maxr2+'$', '$'+"%.3f" % maxr3+'$'])
	else:
		files = os.listdir('../rankings/'+method+'/')
		for file in sorted(files):
			prefix = file[6:len(file)-4]
			subs = []
			f = open('../rankings/'+method+'/'+file)
			for line in f:
				subs.append(line.strip().split('\t'))
			f.close()					
			t1, t2, t3, r1, r2, r3 = re.evaluateRanker('../corpora/semeval/semeval_test.txt', subs)
			print(prefix+': t1='+str(t1)+', t2='+str(t2)+', t3='+str(t3))
			#myt.append([prefix[0].upper()+prefix[1:len(prefix)], '$'+"%.3f" % t1+'$', '$'+"%.3f" % t2+'$', '$'+"%.3f" % t3+'$', '$'+"%.3f" % r1+'$', '$'+"%.3f" % r2+'$', '$'+"%.3f" % r3+'$'])
			myt.append([prefix[0].upper()+prefix[1:len(prefix)], '$'+"%.3f" % t1+'$', '$'+"%.3f" % r1+'$', '$'+"%.3f" % r2+'$', '$'+"%.3f" % r3+'$'])
print(tabulate(myt, headers, tablefmt="latex"))
