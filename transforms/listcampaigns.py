# List CRITs Campaigns
# For use with mcrits
# Author: Brian Warehime @nulltr0n
# 11/14/2014

# Importing various modules

from MaltegoTransform import *
import requests
import json
import pprint
import os
import ConfigParser

# Configuration Parser to grab necessary options.

def getLocalConfPath():
   	pathname = os.path.dirname(sys.argv[0])
	pathname = os.path.abspath(pathname)
	pathname = os.path.join(pathname, '..','local', 'mcrits.conf')
	return os.path.normpath(pathname)

def makeRequest(url, params):
	r = requests.get(url, params=params, verify=False)
	j = json.loads(r.text)
	for camp in j['objects']:
		ent = me.addEntity("mcrits.Campaign",camp['name'])
	return j['meta']['next']

configFile = getLocalConfPath()
config = ConfigParser.SafeConfigParser()
config.read(configFile)

username = config.get('info', 'username')
url = config.get('info', 'url')
path = '/api/v1/campaigns/'
api_key = config.get('info', 'api_key')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
me.parseArguments(sys.argv)
host = sys.argv[1]

# Setting up requests variables from mcrits.conf

params = {
'api_key': api_key,
'username': username,
}

next_ = makeRequest(url + path, params)
while next_:
	next_ = makeRequest(url + next_, params)

ent = me.addEntity("mcrits.Campaign",'Unknown')

#Return Maltego Output

me.returnOutput()
