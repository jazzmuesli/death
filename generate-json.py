import sys
import json
import csv

def fix_text(str):
  return str.decode('ascii','ignore')

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

mps = dict()
with open('party-year-area.csv', 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  i = 0
  for row in spamreader:
    i = i+1
    if i == 1:
      continue
    area = row[1]
    year = row[2]
    party = fix_text(row[3])
    cnt = row[4]
    mps[area] = mps.get(area, dict())
    mps[area][year] = mps[area].get(year, dict())
    mps[area][year][party] = cnt

for area in lifeexp:
  for year in lifeexp[area]:
    les = [float(lifeexp[area][year].get(x,0)) for x in ['male','female']]
    if len(les) == 2:
      lifeexp[area][year] = "%.1f" % float(sum(les)/2)

for area in mps:
  for year in mps[area]:
    seats = [int(x) for x in mps[area][year].values()]
    for party in mps[area][year]:
      mps[area][year][party] = "%.2f" % (float(mps[area][year][party]) / sum(seats))
      #mps[area][year][party] = "%.2f" % float(mps[area][year][party])/sum(seats)
    #print seats, sum(seats)
#sys.exit(0)
data = json.loads(file('lad.json').read())
features = data['features']
for i in range(len(features)):
  feature = features[i]
  area = feature['properties']['LAD13CD']
  feature['properties']['lifeexp'] = lifeexp.get(area, dict())
  feature['properties']['mps'] = mps.get(area, dict())
#print mps#, indent=True)
text = json.dumps(data, indent=True) 
print text
#print text.encode('ascii','ignore')
