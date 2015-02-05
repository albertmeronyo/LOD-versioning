#!/usr/bin/env python

import json
from rdflib import Graph, URIRef
from rdflib.namespace import OWL
from rdflib.plugin import PluginException
import urllib2
import logging

logging.basicConfig(level=logging.DEBUG)

ont = {}

f = open("ontologies-uri.json", "r")
jf = json.load(f)
ds = set()
for key,value in jf.iteritems():
	if len(value):
		for r in value:
                        ds.add(r["ontology"]["value"])
logging.debug(ds)
logging.info("Total datasets: %s" % len(ds))

for i, o in enumerate(ds):
        logging.debug("Processing ontology %s out of %s (%s %% done)" % (str(i), str(len(ds)), str(round((float(i)/len(ds))*100, 2))))
        g = Graph()
        try:
                g.parse(o)
        except urllib2.HTTPError:
                logging.debug("URI not found")
                pass
        except PluginException:
                logging.debug("I don't know how to parse this")
                pass
        except Exception:
                logging.debug("Undefined exception: skipping this ontology")
                pass
        logging.info("Ontology %s retrieved correctly, parsed %s triples" % (o, len(g)))
        priorLink = True
        while priorLink:
                # Search for owl:priorVersion
                prior = None
                for s, p, o in g.triples( (None, OWL.priorVersion, None) ):
                        # Is it a URI?
                        prior = URIRef(o)
                        logging.debug("Found link: %s" % prior)
                if prior:
                        if o not in ont:
                                ont[o] = []
                        ont[o].append(prior)
                else:
                        priorLink = False
        logging.debug(ont)
with open('ontology-versions.json', 'wb') as fp:
        json.dump(self.getVersions(), fp)
