from lexenstein.evaluators import *

subs = {}
gen_sel = []
f = open('../../substitutions/all/substitutions.txt')
for line in f:
        data = line.strip().split('\t')
        word = data[0].strip()
        cands = set(data[1].strip().split('|||'))
        subs[word] = cands
f.close()

f = open('../../substitutions/all/substitutions_void.txt')
subs_void = {}
void_sel = []
for line in f:
	data = line.strip().split('\t')
	items = data[3:len(data)]
	cands = set([item.strip().split(':')[1].strip() for item in items])
	target = data[1].strip()
	if target in subs_void.keys():
		subs_void[target] = subs_void[target].union(cands)
	else:
		subs_void[target] = cands	
	void_sel.append(cands)
	gens = subs[target]
	gen_sel.append(gens)
	diff = gens.difference(cands)
	diff1 = cands.difference(gens)
	if len(diff)>0 or len(diff1)>0:
		print('Problem at: ' + target)
		print('Gens-Cands: ' + str(diff))
		print('Cands-Gens: ' + str(diff1))
f.close()

ge = GeneratorEvaluator()
po, pr, re, fm = ge.evaluateGenerator('../../corpora/lexmturk_gold.txt', subs)
print('For Gen: ' + str(po) + ' ' + str(pr) + ' ' + str(re) + ' ' + str(fm))
po, pr, re, fm = ge.evaluateGenerator('../../corpora/lexmturk_gold.txt', subs_void)
print('For Void: ' + str(po) + ' ' + str(pr) + ' ' + str(re) + ' ' + str(fm))

se = SelectorEvaluator()
po, pr, re, fm = se.evaluateSelector('../../corpora/lexmturk_gold.txt', gen_sel)
print('For Gen: ' + str(po) + ' ' + str(pr) + ' ' + str(re) + ' ' + str(fm))
po, pr, re, fm = se.evaluateSelector('../../corpora/lexmturk_gold.txt', void_sel)
print('For Void: ' + str(po) + ' ' + str(pr) + ' ' + str(re) + ' ' + str(fm))
