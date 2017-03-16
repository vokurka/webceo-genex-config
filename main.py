import csv, pip, pprint, json
from keboola import docker
pip.main(['install', 'requests'])
import requests

# Getting configuration
cfg = docker.Config('/data/')
parameters = cfg.get_parameters()
config = {}
configFields = ['#sapi_token', '#webceo_token', 'component_id', 'config_id']

for field in configFields:
	config[field] = parameters.get(field)

	if not config[field]:
		raise Exception('Missing mandatory configuration field: '+field)

# Loading list of projects I want to generate the configuration for
projects = list(csv.DictReader(open('/data/in/tables/projects.csv', 'r', encoding='utf-8')))

# Base part of configuration - envelope
genex_config = {
  "parameters": {
    "api": {
      "baseUrl": "https://online.webceo.com/",
      "name": "webceo"
    },
    "config": {
      "id": "webceo",
      "debug": 1,
      "jobs": "placeholder"
    }}}

# List of all generated jobs
jobs = []

# Go through all projects and for each one create a job
for p in projects:
	jobs.append({
      "endpoint": "api/",
      "dataType": "rankings",
      "dataField": ".",
      "method": "POST",
      "params": {
        "method": "get_rankings",
        "key": config['#webceo_token'],
        "data": {
          "project": p['project']
     }}})

# Put the jobs array to the correct place in GenEx configuration envelope
genex_config['parameters']['config']['jobs'] = jobs;

# Update the configuration in KBC
r = requests.put("https://connection.keboola.com/v2/storage/components/"+config['component_id']+"/configs/"+config['config_id'],
	headers={"X-StorageApi-Token": config['#sapi_token']}, 
	files=dict(name='WebCEO Rankings', configuration=json.dumps(genex_config)
	))