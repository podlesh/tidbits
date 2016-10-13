#!/usr/bin/python

#
# convert text files with month names to single CSV
# each name is presented in original form and with removed accents (if there are any accents, of course)
#
#  files must conform to nameing convention:
#    language[-variant].extension
#  for example: cs.txt, cs-gen.txt, fi.txt
#

import sys
import unicodedata
import codecs
import csv
import os
import re

def remove_accents(input_str):
  nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
  return u"".join(c for c in nkfd_form if not unicodedata.combining(c))

numbers = range(1,13)

result = dict()
def add_result(month, num, lang):
	if month in result:
		oldnum,oldlangs = result[month]
		if oldnum<>num:
			print "ERROR: duplicit month %s with numbers %d and %d" % (month, num, oldnum)
			sys.exit(-1)
		if not lang in oldlangs:
			oldlangs.append(lang)
	else:
		result[month] = (num, [lang])
	

for fn in sys.argv[1:]:
  with codecs.open(fn, 'r', encoding='utf-8') as f:
    fn_base = re.sub(r'[^a-zA-Z].*$', '', os.path.basename(fn))
    months = f.readlines()
    assert len(months)==12
    for month, num in zip([m.strip() for m in months], numbers):
    	stripped = remove_accents(month)
    	add_result(month, num, fn_base)
	if stripped<>month:
		add_result(stripped, num, fn_base)

rows_utf8 = [
	[name.encode('utf-8'), num, "+".join(lang)]
	for name, (num, lang) in result.iteritems()
]
rows_utf8.sort(key=lambda x: x[1:])

out = csv.writer(sys.stdout, lineterminator='\n', delimiter=';')
out.writerows(rows_utf8)

