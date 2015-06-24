
ost = open('source_target.txt', 'w')
ots = open('target_source.txt', 'w')

fn = open('../../corpora/wiki/normal.ascii.aligned')
fs = open('../../corpora/wiki/simple.ascii.aligned')

for linen in fn:
	lines = fs.readline()
	datan = linen.strip().split('\t')
	datas = lines.strip().split('\t')
	if len(datan)>2 and len(datas)>2:
		sentn = linen.strip().split('\t')[2].strip()
		sents = lines.strip().split('\t')[2].strip()
		ost.write(sentn + '\t' + sents + '\n')
		ots.write(sents + '\t' + sentn + '\n')
fn.close()
fs.close()

fn = open('../../corpora/wiki/wiki.unsimplified')
fs = open('../../corpora/wiki/wiki.simple')
for linen in fn:
	lines = fs.readline()
	sentn = linen.strip()
	sents = lines.strip()
	ost.write(sentn + '\t' + sents + '\n')
	ots.write(sents + '\t' + sentn + '\n')
fn.close()
fs.close()

ost.close()
ots.close()
