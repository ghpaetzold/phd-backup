import sys, os

size = sys.argv[1]
senseaware = sys.argv[2]
if senseaware=='0':
        senseaware = False
elif senseaware=='1':
        senseaware = True
else:
        print('senseaware parameter not recognized!')
arch = sys.argv[3]

#Create common vectors path:
vectors = '../../corpora/wordvectors/wordnet'
if senseaware:
        vectors += 'parsed'
else:
        vectors += 'orig'
vectors += size+'_vectors_'+arch+'.txt'

#Get retrofitted file:
retrofitted = '../../corpora/wordvectors/retrofitted_wordnet'
if senseaware:
        retrofitted += 'parsed'
else:
        retrofitted += 'orig'
retrofitted += size+'_vectors_'+arch+'.txt'

#Create lexicon path:
wnlexicon = '../../lexicons/wordnet-synonyms.txt'
if senseaware:
        wnlexicon = '../../lexicons/parsed-wordnet-synonyms.txt'

#Get iters:
iters = '100'

#Create command line:
comm = 'nohup python ../retrofitting/retrofit.py -i ' + vectors + ' -l ' + wnlexicon + ' -o ' + retrofitted + ' -n ' + iters + ' &'
os.system(comm)
