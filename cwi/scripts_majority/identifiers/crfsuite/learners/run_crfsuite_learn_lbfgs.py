import os

import os

os.system('mkdir ../models/lbfgs/')

#Parameters:
mems = ['6', '10']
cs = ['0', '1']
maxiters = ['200', '300']
stops = ['10', '20']
lines = ['20', '30']

for mem in mems:
	for line in lines:
		for c in cs:
			for maxiter in maxiters:
				comm = 'nohup /export/tools/crfsuite/bin/crfsuite learn -m '
				comm += '../models/lbfgs/'+str(mem)+'_'+str(line)+'_'+str(c)+'_'+str(maxiter)+'.txt --algorithm='
				comm += 'lbfgs '
				comm += '--set=num_memories=' + str(mem) + ' '
				comm += '--set=c1=' + str(c) + ' '
				comm += '--set=c2=' + str(1-int(c)) + ' '
				comm += '--set=max_linesearch=' + str(line) + ' '
				comm += '--set=max_iterations=' + str(maxiter) + ' '
				comm += '../datasets/training_simplified.txt &'
				print(comm)
				os.system(comm)
