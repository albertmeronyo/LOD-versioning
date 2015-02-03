#!/usr/bin/env python

f = open("datasets.json", "r")
jf = json.load(f)
ds = {}
for key,value in jf.iteritems():
    for e in value:
        if e[0] not in ds:      
            ds[e[0]] = []
        else:
            ds[e[0]].append(e[1])
print ds
