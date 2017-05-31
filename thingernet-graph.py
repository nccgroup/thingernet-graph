#!/usr/bin/env python

'''
Released as open source by NCC Group Plc - http://www.nccgroup.trust/
Developed by Matt Lewis, matt dot lewis at nccgroup dot trust

https://github.com/m4ttl/thingernet-graph

Released under AGPL see LICENSE for more information

Synopsis - reads a directory of JSON files describing 'things' and creates the
relevant neo4j cypher text for import to neo4j in order to produce a graph 
database representation of the 'thingernet' - a directed graph with node and edge
properties that allow us to reason about, and appraise the security of thingernets.
'''

import json
import glob
import sys

#
# A container for a 'Thing'
#
class Thing:
    def __init__(self, name, position, encryption, data, effect):
        self.name = name		
        self.position = position	# mobile or static
        self.encryption = encryption    # this value refers to encryption 'at rest'
        self.data = data                # what type of data is stored in this thing?
        self.effect = effect            # what is the thing's effect on its environment?
	self.thingabilities = {}	# interfaces

    def printer(self):
        print "CREATE (%s:Thing {name:\'%s\', position:\'%s\', encryption:\'%s\', data:\'%s\', effect:\'%s\'})" \
                % (self.name, self.name, self.position, self.encryption, self.data, self.effect)

#
# A container for a Thing's Thingabilities
#
class Thingability:
    def __init__(self, conntype, auth, direction, protocol, crypto):
	self.conntype = conntype	# wired or wireless
	self.auth = auth		# authenticated or not
	self.direction = direction	# TX, RX or both (TXRX)
	self.protocol = protocol	# top-level protocol
        self.crypto = crypto            # encryption at rest

#
# load a json file of a Thing and its Thingabilities
#
def GetThing(filename):
    with open(filename) as data_file:
	data = json.load(data_file)

    data_file.close()

    for thing in data["thing"]:
	newthing = Thing(thing["name"], thing["position"], thing["encryption"], thing["data"], thing["effect"])
	for interface in thing["interfaces"]:
	    thingability = Thingability(interface["conntype"],interface["auth"],interface["direction"],\
                    interface["protocol"],interface["crypto"])
	    newthing.thingabilities[interface["interface"]] = thingability
    
    return newthing

#
# read all json things in a folder into a list of things
#
def GetThings(directory):
    Thingernet = []
    files = glob.glob(directory + '/*.json')
   
    if len(files) == 0:
        print "No json files found in specified directory: {0}".format(directory)
        exit(1)

    for f in files:
	Thingernet.append(GetThing(f))
	
    return Thingernet

#
# match the thingertivity between all things in our thingernet
#
def Thingertivity(thingernet):
    numThings = len(thingernet)
    if numThings > 1:
        i = 0
	while i < numThings:
	    currentThing = thingernet[i]
	    for thing in thingernet:
	        if currentThing != thing:
		    for (ifaceA, propertiesA) in currentThing.thingabilities.items():
		        for (ifaceB, propertiesB) in thing.thingabilities.items():
			    if ifaceA == ifaceB:
			        if 'TX' in propertiesA.direction  and 'RX' in propertiesB.direction:
                                    print "CREATE (%s)-[:%s {conntype: \'%s\', auth: \'%s\', crypto: \'%s\'}]->(%s)" \
                                            % (currentThing.name,ifaceA,propertiesA.conntype,propertiesA.auth,propertiesA.crypto,thing.name)

			    if ifaceA == 'Speaker' and ifaceB == 'Microphone': 
                                print "CREATE (%s)-[:%s {conntype: \'%s\', auth: \'%s\', crypto: \'%s\'}]->(%s)" \
                                        % (currentThing.name,"Sound",propertiesA.conntype,propertiesA.auth,propertiesA.crypto,thing.name)
	    i += 1
    else:
        print "Only 1 or less things so no thingertivity"
        
#
# bring everything together and print our cypher text for neo4j
#
def getCypher(jsondir):
    thingernet = GetThings(jsondir)

    for thing in thingernet:
        thing.printer()

    Thingertivity(thingernet)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: {0} <directory of \'json\' thing files>".format(sys.argv[0])
        exit(0)
    else:
        try:
            jsondir = sys.argv[1]
            getCypher(jsondir)
        except IOError as e:
            print "Error {0}: {1}".format(e.errno, e.strerror)
            
