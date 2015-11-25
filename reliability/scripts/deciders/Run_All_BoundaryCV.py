import os

#Problems;
problems = ['paetzold_boundaryUnsupervisedCV_subimdb00.txt']

#Parameters:
positive_ranges = ['1']
folds = ['10']
test_sizes = ['0.25']

for problem in problems:
	for p in positive_ranges:
		for f in folds:
			for t in test_sizes:
				comm = 'nohup python Run_BoundaryCV.py ../../../sr_userstudy/corpora/NNSimpLex.txt '+p+' '+f+' '+t
				comm += ' '+problem+' &'
				os.system(comm)
