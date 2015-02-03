#!/usr/bin/env python
# *-* encoding: utf-8 -*-

# LODVersions.py: a crawler of different versions of datasets
# in the LOD cloud.

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound, EndPointInternalError
import urllib2
from httplib import BadStatusLine
from simplejson import JSONDecodeError
import socket
import time
from xml.parsers.expat import ExpatError
from ConfigParser import SafeConfigParser
import logging
import json
from timeout import timeout, TimeoutError

CONFIG_INI = "config.ini"

class LODVersions:
    endpoints = []
    datasets = {}
    
    def __init__(self, __config):
        self.log = logging.getLogger('LODVersions')

        self.config = __config

        self.log.info("Getting endpoint list...")
        self.initEndpoints()
        self.log.debug(self.getEndpoints())
        self.log.info("Querying endpoints...")
        self.queryEndpoints()
        
        self.log.info(self.getDatasets())
        self.log.info("Serializing retrieved data...")
        self.serializeDatasets()

    def initEndpoints(self):
        '''
        Gets a list of SPARQL endpoint URLs from datahub.io
        '''
        datahub_api_call = self.config.get('datahub', 'api_call')
        datahub_stream = urllib2.urlopen(datahub_api_call)
        datahub_json = json.load(datahub_stream)
        datahub_results = datahub_json["results"]
        for endpoint in datahub_results:
            self.endpoints.append(endpoint["url"])

    def getEndpoints(self):
        '''
        Returns a list with endpoint URLs
        '''
        return self.endpoints

    def queryEndpoints(self):
        '''
        Queries all endpoints using config query
        '''
        for endpoint in self.endpoints:
            self.datasets[endpoint] = []
            try:
                results = self.queryEndpoint(endpoint, self.config.get('sparql', 'query'))
            except TimeoutError:
                self.log.debug("Endpoint timeout")
                pass
            except ValueError:
                self.log.debug("Endpoint and query combination are malformed")
                pass
            if isinstance(results, dict) and "results" in results and "bindings" in results["results"]:
                for r in results["results"]["bindings"]:
                    self.datasets[endpoint].append(r)

    def getDatasets(self):
        '''
        Gets a dict of LOD cloud datasets (key = endpoint url, value = [ results ] )
        '''
        return self.datasets

    def serializeDatasets(self):
        '''
        Serializes retrieved datasets in a json file
        '''
        with open(self.config.get('general', 'dump_file'), 'wb') as fp:
            json.dump(self.getDatasets(), fp)

    @timeout()
    def queryEndpoint(self, url, query):
        '''
        Queries one endpoint 'url' using 'query' as query
        '''
        endpoint_results = None
        wrapper = SPARQLWrapper(url)
        wrapper.setQuery(query)
        wrapper.setReturnFormat(JSON)
        try:
            endpoint_results = wrapper.query().convert()
        except urllib2.URLError:
            self.log.debug("The endpoint URL could not be opened")
            pass
        except EndPointNotFound:
            self.log.debug("Endpoint not found")
            pass
        except EndPointInternalError:
            self.log.debug("There was an internal error at the endpoint")
            pass
        except QueryBadFormed:
            self.log.debug("The endpoint does not like the query")
            pass
        except JSONDecodeError:
            self.log.debug("Could not decode returned JSON")
            pass
        except socket.error:
            self.log.debug("Connection reset by peer")
            pass
        except ExpatError:
            self.log.debug("The endpoint returned XML instead of JSON")
            pass
        except BadStatusLine:
            self.log.debug("The endpoint returned bad HTTP")
            pass
        return endpoint_results

if __name__ == "__main__":
    # Config
    config = SafeConfigParser()
    config.read(CONFIG_INI)
    
    # Logging
    logLevel = logging.INFO
    if config.get('general', 'verbose'):
        logLevel = logging.DEBUG
    logging.basicConfig(level=logLevel)
    logging.info("Initializing...")

    # Instance
    l = LODVersions(config)
    logging.info("Exiting...")
    exit(0)
