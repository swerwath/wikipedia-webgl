import argparse
import math
import json

parser = argparse.ArgumentParser(description='Parse prepared SQL to JSON for Wikipedia location data')
parser.add_argument('-i', '--input')
args = parser.parse_args()

types_to_find = {'glacier':'Glaciers', 'city':'Cities', 'landmark':'Landmarks', 'edu':'Educational', 'mountain':'Mountains', 'airport':'Airports', 'event':'Events'}
types = {'all_types':{}}
for k,v in types_to_find.iteritems():
    types[v] = {}

with open(args.input) as f:
    for line in f:
        if line[0].isdigit():
            data = line.split(',')
            if data[2] == '\'earth\'':
                lat = math.ceil(float(data[4]) * 100) / 100
                lon = math.ceil(float(data[5]) * 100) / 100
                types['all_types'][(lat, lon)] = types['all_types'][(lat, lon)] + 1 if (lat, lon) in types['all_types'] else 1
                if data[7][1:-1] in types_to_find:
                    label = types_to_find[data[7][1:-1]]
                    types[label][(lat, lon)] = types[label][(lat, lon)] + 1 if (lat, lon) in types[label] else 1

for k, v in types.iteritems():
    json_obj = {k:[]}
    for loc, mag in v.iteritems():
        json_obj[k].append(loc[0])
        json_obj[k].append(loc[1])
        json_obj[k].append(mag)
    json_string = json.dumps(json_obj)
    target = 'data/processed/json/' + k + '.json'
    with open(target, 'w') as f:
        f.truncate()
        f.write(json_string)
