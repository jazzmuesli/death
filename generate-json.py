import sys
import json
import csv
lifeexp = dict()
with open('lifeexp-1991-2010.csv', 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    area = row[1]
    year = row[2]
    gender = row[3]
    le = row[4]
    lifeexp[area] = lifeexp.get(area, dict())
    lifeexp[area][year] = lifeexp[area].get(year, dict())
    lifeexp[area][year][gender] = le

data = json.loads(file('lad.json').read())
features = data['features']
for i in range(len(features)):
  feature = features[i]
  area = feature['properties']['LAD13CD']
  feature['lifeexp'] = lifeexp.get(area, dict())
print json.dumps(data, indent=True) 
