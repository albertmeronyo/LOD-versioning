#!/usr/bin/env python

import json

f = open("ontologies.json", "r")
jf = json.load(f)
ds = {}
for key,value in jf.iteritems():
	if len(value):
		for r in value:
			if r["ontology"]["value"] not in ds:
				ds[r["ontology"]["value"]] = []
			if r["priorVersion"]["value"] not in ds[r["ontology"]["value"]]:
				ds[r["ontology"]["value"]].append(r["priorVersion"]["value"])
print ds
print "Total datasets: %s" % len(ds)

count1 = 0
count2 = 0
count3m = 0
valuable = []
for key,value in ds.iteritems():
	if len(value) == 1:
		count1 += 1
	elif len(value) == 2:
		count2 += 1
	elif len(value) >= 3:
		count3m += 1
		valuable.append([key, sorted(value)])

print "Datasets with one version: %s" % count1
print "Datasets with two versions: %s" % count2
print "Datasets with three+ versions: %s" % count3m
for v in sorted(valuable):
	print v
