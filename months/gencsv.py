#!/usr/bin/python

import sys
import unicodedata
import codecs
import csv
import os
import re

def remove_accents(input_str):
  nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
  return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

numbers = range(1,13)

result = []

for fn in sys.argv[1:]:
  with codecs.open(fn, 'r', encoding='utf-8') as f:
    fn_base = re.sub(r'[^a-zA-Z].*$', '', os.path.basename(fn))
    months = f.readlines()
    assert len(months)==12
    for month, num in zip([m.strip() for m in months], numbers):
    	stripped = remove_accents(month)
    	result.append([month, str(num), fn_base])
	if stripped<>month:
		result.append([stripped,str(num),fn_base])

rows_utf8 = [
	[s.encode('utf-8') for s in row]
	for row in result
]

out = csv.writer(sys.stdout)
out.writerows(rows_utf8)

