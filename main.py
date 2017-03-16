import csv, pip, pprint
from keboola import docker

# Getting configuration
cfg = docker.Config('/data/')
parameters = cfg.get_parameters()
config = {}
configFields = ['#sapi_token', '#webceo_token']

for field in configFields:
	config[field] = parameters.get(field)

	if not config[field]:
		raise Exception('Missing mandatory configuration field: '+field)

projects = list(csv.DictReader(open('/data/in/tables/projects.csv', 'r', encoding='utf-8')))