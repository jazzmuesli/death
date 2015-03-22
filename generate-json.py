import sys
import json
import csv

def fix_text(str):
  return str.decode('ascii','ignore')
def derive_party(party):
  parties = ["conservative","labour","liberal"]
  for p in parties:
    if p in party.lower():
      return p
  if "Speaker" in party:
    return 'conservative'
  return "other"
lifeexp = dict()
with open('lifeexp-1991-2010.csv', 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  i = 0
  for row in spamreader:
    i = i+1
    if i == 1:
      continue
    area = row[1]
    year = int(row[2])
    if year < 1992:
      continue
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
    year = int(row[2])
    party = derive_party(fix_text(row[3]))
    cnt = row[4]
    mps[area] = mps.get(area, dict())
    mps[area][year] = mps[area].get(year, dict())
    mps[area][year][party] = cnt

le_map = dict()
for area in lifeexp:
  for year in lifeexp[area]:
    les = [float(lifeexp[area][year].get(x,0)) for x in ['male','female']]
    if len(les) == 2:
      le = float("%.1f" % float(sum(les)/2))
      x = le_map.get(year, [])
      x.append(le)
      le_map[year]= x
      lifeexp[area][year] = le
for area in lifeexp:
  for year in lifeexp[area]:
    x = lifeexp[area][year]
    #g = (x-min(le_list))/(max(le_list)-min(le_list))
    g = (x - min(le_map[year])) / (max(le_map[year])-min(le_map[year]))
    #print x, g, min(le_list), max(le_list)
    lifeexp[area][year] = float("%.2f" % g)
    
area_seats = dict()
for area in mps:
  for year in mps[area]:
    seats = [int(x) for x in mps[area][year].values()]
    for party in mps[area][year]:
      proportion = float("%.2f" % (float(mps[area][year][party]) / sum(seats)))
      mps[area][year][party] = proportion
      area_seats[area] = area_seats.get(area, [])
      area_seats[area].append(proportion)
      #mps[area][year][party] = "%.2f" % float(mps[area][year][party])/sum(seats)
    #print seats, sum(seats)
#for area in area_seats:
#  seats = area_seats[area]
#  print sum(seats)/len(seats) < 1.0
#print json.dumps(area_seats, indent=True)
#sys.exit(0)
data = json.loads(file('lad.json').read())
features = data['features']
new_features = []
for i in range(len(features)):
  feature = features[i]
  area = feature['properties']['LAD13CD']
  try:
    feature['properties']['lifeexp'] = lifeexp[area]#.get(area, dict())
    feature['properties']['mps'] = mps[area]#.get(area, dict())
    x = feature['properties']['mps']
    new_features.append(feature)
  except:
    pass
  #for year in x:
    #print "\n".join(x[year].keys())
  #print ["\n".join(x.keys()) for x in feature['properties']['mps'].values()]
#print mps#, indent=True)
#E06000053
data['features'] = new_features
text = json.dumps(data, indent=True) 
print "var  localAuthorities =", text + ";"
#print text.encode('ascii','ignore')
