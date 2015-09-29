import os

os.system('mkdir ../../../../corpora/wcefiles/models/')
os.system('mkdir ../../../../corpora/wcefiles/models/pa/')

#Parameters:
types = ['0', '1', '2']
cs = ['0.1', '1', '10']
maxiters = ['100', '200', '300']
maxiters = ['500', '600']

for type  in types:
	for c in cs:
		for maxiter in maxiters:
			comm = 'nohup /export/tools/crfsuite/bin/crfsuite learn -m '
			comm += '../../../../corpora/wcefiles/models/pa/'+str(type)+'_'+str(c)+'_'+str(maxiter)+'.txt --algorithm='
			comm += 'pa '
			comm += '--set=type=' + str(type) + ' '
			comm += '--set=c=' + str(c) + ' '
			comm += '--set=max_iterations=' + str(maxiter) + ' '
			comm += '../../../../corpora/wcefiles/training.txt &'
			print(comm)
			os.system(comm)
