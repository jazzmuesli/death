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

for area in lifeexp:
  for year in lifeexp[area]:
    les = [float(lifeexp[area][year].get(x,0)) for x in ['male','female']]
    if len(les) == 2:
      lifeexp[area][year] = "%.1f" % float(sum(les)/2)
data = json.loads(file('lad.json').read())
features = data['features']
for i in range(len(features)):
  feature = features[i]
  area = feature['properties']['LAD13CD']
  feature['properties']['lifeexp'] = lifeexp.get(area, dict())
print json.dumps(data, indent=True) 
