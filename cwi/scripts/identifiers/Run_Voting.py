import sys

train_victor_corpus = sys.argv[1]
k = int(sys.argv[2].strip())
use_f = False
if sys.argv[3].strip()=='True':
	use_f = True
test_victor_corpus = sys.argv[4].strip()
out_file = sys.argv[5].strip()

f = open('../evaluators/best_cwi.txt')
scores = {}
for line in f:
	data = line.strip().split('\t')
	file = data[1].strip()
	score = float(data[2].strip())
	name = data[0].strip()
	if name!='voting':
		scores[(name, file)]=score
ranked = sorted(scores.keys(), key=scores.__getitem__, reverse=True)

limit = min(len(ranked), k)

files = []
scoresv = []
for i in range(0, limit):
	files.append(open('../../labels/'+ranked[i][0]+'/'+ranked[i][1]))
	scoresv.append(scores[ranked[i]])

o = open(out_file, 'w')
inp = open(test_victor_corpus)
for line in inp:
	s0 = 0
	s1 = 0
	for i in range(0, len(files)):
		file = files[i]
		score = scoresv[i]
		label = file.readline().strip()

		multiplier = 1
		if use_f:
			multiplier = score
		if label=='1':
			s1+=multiplier
		else:
			s0+=multiplier
	if s0>s1:
		o.write('0\n')
	else:
		o.write('1\n')
o.close()
inp.close()

for file in files:
	file.close()
