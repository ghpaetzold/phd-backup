import os

os.system('mkdir ../../../../corpora/wcefiles/models/')
os.system('mkdir ../../../../corpora/wcefiles/models/arow/')

#Parameters:
vars = [0.01, 10]
gammas = [0.01, 10]
maxiters = ['200', '500']

for var in vars:
	for gamma in gammas:
		for maxi in maxiters:
			comm = 'nohup /export/tools/crfsuite/bin/crfsuite learn -m '
			comm += '../../../../corpora/wcefiles/models/arow/'+str(var)+'_'+str(gamma)+'_'+str(maxi)+'.txt --algorithm=arow '
			comm += '--set=variance=' + str(var) + ' '
			comm += '--set=gamma=' + str(gamma) + ' '
			comm += '--set=max_iterations='+maxi+' '
			comm += '../../../../corpora/wcefiles/training.txt &'
			print(comm)
			os.system(comm)
