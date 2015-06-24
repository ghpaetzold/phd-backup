import urllib.request as urllib
import xml.etree.ElementTree as ET
import re

lex = open('../../../corpora/lexmturk/lexmturk.txt')
out = open('../../../corpora/substitutions/merriam/substitutions.txt', 'w', encoding='utf-8')
for line in lex:
	data = line.strip().split('\t')
	target = data[1].strip()
	url = 'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/' + target + '?key=c21550b0-418e-4a52-b85c-76587b8fdc2f'
	conn = urllib.urlopen(url)
	root = ET.fromstring(conn.read())
	root = root.findall('entry')
	if len(root)>0:
		root = root[0]
		for sense in root.iter('sens'):
			syn = sense.findall('syn')[0]
		res = ''
		for snip in syn.itertext():
			res += snip + ' '

		finds = re.findall('\([^\)]+\)', res)
		for find in finds:
			res = res.replace(find, '')

		syntext = ''
		synonyms = res.split(',')
		for synonym in synonyms:
			syntext += synonym.strip() + '|||'
		syntext = syntext[0:len(syntext)-3]
		out.write(target + '\t' + syntext + '\n')
	else:
		out.write(target + '\t\n')
lex.close()
out.close()
