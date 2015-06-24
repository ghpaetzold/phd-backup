import os

Cs = [0.0001, 0.001, 0.01, 0.1, 1, 10]
epsilons = [0.00001, 0.0001, 0.001, 0.01]
kernels = [0, 1, 2, 3]

for C in Cs:
	for e in epsilons:
		for k in kernels:
			comm = 'nohup /export/tools/svm-rank/svm_rank_learn -c ' + str(C) + ' -e ' + str(e) + ' -t ' + str(k)
			comm += ' ./features/training_features.txt ' + './models/model_'+str(C)+'_'+str(e)+'_'+str(k)+'.dat &'
			print(str(comm))
			os.system(comm)

