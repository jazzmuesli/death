import codecs
import io
import time
import re
from lxml import html
import requests
import sys

writer = open('result.csv', 'w')
data = open('index.html').read()
tree = html.fromstring(data)

items = tree.xpath('//tr[contains(@id, "trItemRow")]/td/text()')
items = [x.rstrip().lstrip() for x in items] 
for i in range(1,len(items),3):
  line = items[i+1] + "," + items[i]
  writer.write(line.enecode('ascii','ignore')+"\n")
