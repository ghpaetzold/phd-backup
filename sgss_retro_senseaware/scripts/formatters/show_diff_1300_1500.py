targets = []
gold = []
f = open('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt')
for line in f:
	data = line.strip().split('\t')
	cands = set([word.strip().split(':')[1].strip() for word in data[3:]])
	target = data[1]
	targets.append(target)
	gold.append(cands)
f.close()

subs = {}
subs1300 = []
f = open('../../substitutions/paetzold_retrofitted1300/substitutions.txt')
for line in f:
	data = line.strip().split('\t')
	target = data[0].strip()
	cands = set(data[1].strip().split('|||'))
	subs[target] = cands
f.close()
for target in targets:
	if target in subs:
		subs1300.append(subs[target])
	else:
		subs1300.append(set([]))

subs = {}
subs1500 = []
f = open('../../substitutions/paetzold_retrofitted1500/substitutions.txt')
for line in f:
        data = line.strip().split('\t')
        target = data[0].strip()
        cands = set(data[1].strip().split('|||'))
        subs[target] = cands
f.close()
for target in targets:
        if target in subs:
                subs1500.append(subs[target])
        else:
                subs1500.append(set([]))

explained = 0
pot13 = 0
pot15 = 0
for i in range(len(gold)):
	g = gold[i]
	c13 = subs1300[i]
	c15 = subs1500[i]

	good13 = g.intersection(c13)
	good15 = g.intersection(c15)
	miss15 = good13.difference(c15)
	bad15 = c15.difference(g)
	bad13 = c13.difference(g)

	if len(miss15.difference(good13))==0 and len(miss15)>0:
		explained += 1
	if len(good13)>0:
		pot13 += 1
	if len(good15)>0:
		pot15 += 1

	print('\nTarget: ' + targets[i])
	print('Good 13: ' + str(sorted(list(good13))))
	print('Good 15: ' + str(sorted(list(good15))))
	print('Miss 15: ' + str(sorted(list(miss15))))
	print('Bad 13: ' + str(sorted(list(bad13))))
	print('Bad 15: ' + str(sorted(list(bad15))))

print('\nPot 13: ' + str(float(pot13)/len(gold)))
print('Pot 15: ' + str(float(pot15)/len(gold)))
print(str(explained))
