f = open('../../corpora/cwi_training_multitask.txt')

languages = set([])
educations = set([])
proficiencies = set([])
for line in f:
	data = line.strip().split('\t')
	anns = data[3:]
	for ann in anns:
		annd = ann[1:len(ann)-1].split(', ')
		languages.add(annd[1])
		educations.add(annd[2])
		proficiencies.add(annd[3])
f.close()

o = open('../../corpora/age_tasks.txt', 'w')
o.write('20\n30\n40\n50\n60')
o.close()

o = open('../../corpora/language_tasks.txt', 'w')
for w in languages:
	o.write(w + '\n')
o.close()

o = open('../../corpora/education_tasks.txt', 'w')
for w in educations:
        o.write(w + '\n')
o.close()

o = open('../../corpora/proficiency_tasks.txt', 'w')
for w in proficiencies:
        o.write(w + '\n')
o.close()
