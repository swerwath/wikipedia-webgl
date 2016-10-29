import argparse
import math
import json

parser = argparse.ArgumentParser(description='Parse prepared SQL to JSON for Wikipedia location data')
parser.add_argument('-i', '--input')
parser.add_argument('-r', '--rounding')
args = parser.parse_args()

rounding_factor = 10 ** int(args.rounding)

types_to_find = {'glacier':'Glaciers', 'city':'Cities', 'edu':'Educational', 'mountain':'Mountains', 'airport':'Airports', 'event':'Events'}
types = {}
for k,v in types_to_find.iteritems():
    types[v] = {}

with open(args.input) as f:
    for line in f:
        if line[0].isdigit():
            data = line.split(',')
            if data[2] == '\'earth\'':
                lat = math.ceil(float(data[4]) * rounding_factor) / rounding_factor
                lon = math.ceil(float(data[5]) * rounding_factor) / rounding_factor
                if data[7][1:-1] in types_to_find:
                    label = types_to_find[data[7][1:-1]]
                    types[label][(lat, lon)] = types[label][(lat, lon)] + 1 if (lat, lon) in types[label] else 1

json_obj = []
for k, v in types.iteritems():
    json_obj.append([k, []])
    for loc, mag in v.iteritems():
        json_obj[-1][-1].append(loc[0])
        json_obj[-1][-1].append(loc[1])
        json_obj[-1][-1].append(mag)

json_string = json.dumps(json_obj)
target = 'data/processed/data.json'
with open(target, 'w') as f:
    f.truncate()
    f.write(json_string)
