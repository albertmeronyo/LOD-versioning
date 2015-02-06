#!/usr/bin/env python

import json
from rdflib import Graph

f = open("ontologies.json", "r")
jf = json.load(f)
ds = []
for key,value in jf.iteritems():
	if len(value):
		for r in value:
                        ont = r["ontology"]["value"]
                        prior = r["priorVersion"]["value"]
                        if len(ont) == 0 or len(prior) == 0:
                                continue                        
                        ds.append([ont, prior])
print ds
print "Total datasets: %s" % len(ds)

ontList = []
pairDone = False
for pair in ds:
        for chain in ontList:
                if pair[0] in chain and pair[1] not in chain:
                        chain.insert(chain.index(pair[0]), pair[1])
                        pairDone = True
                        break
                if pair[1] in chain and pair[0] not in chain:
                        chain.insert(chain.index(pair[1]) - 1, pair[0])
                        pairDone = True
                        break
                if pair[0] in chain and pair[1] in chain:
                        pairDone = True
                        break
        if not pairDone:
                ontList.append(pair)
        pairDone = False

print ontList

count1 = 0
count2 = 0
count3m = 0
valuable = []
for chain in ontList:        
	if len(chain) == 1:
		count1 += 1
	elif len(chain) == 2:
		count2 += 1
	elif len(chain) >= 3:
		count3m += 1
		valuable.append(chain)

print "Datasets with one version: %s" % count1
print "Datasets with two versions: %s" % count2
print "Datasets with three+ versions: %s" % count3m
for v in sorted(valuable):
	print v

# From valuable, we try to dereference them...
available = []
for chain in valuable:
        print "Processing chain %s" % chain
        aChain = []
        for o in chain:
                g = Graph()
                try:
                        g.parse(o)
                        aChain.append(o)
                except Exception:
                        print "FATAL, ontology %s is unavailable" % o
        if len(aChain) >= 3:
                available.append(aChain)
print available
json.dumps(available, "cool-chains.json")
