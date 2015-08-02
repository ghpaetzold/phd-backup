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
	scores[(data[0].strip(), file)]=score
ranked = sorted(scores.keys(), key=scores.__getitem__, reverse=True)

limit = min(len(ranked), k)

files = []
scoresv = []
for i in range(0, limit):
	print(str(ranked[i]))
	files.append(open('../../labels/'+ranked[i][0]+'/'+ranked[i][1]))
	scoresv.append(scores[ranked[i]])

o = open(out_file, 'w')
inp = open(test_victor_corpus)
for line in inp:
	maxlabel = None
	maxproba = -1.0
	for i in range(0, len(files)):
		file = files[i]
		score = scoresv[i]
		labeld = file.readline().strip().split('\t')
		label = labeld[0].strip()
		proba = float(labeld[1].strip())

		if proba>maxproba:
			maxproba = proba
			maxlabel = label

	o.write(maxlabel+'\t'+str(maxproba)+'\n')
o.close()
inp.close()

for file in files:
	file.close()
