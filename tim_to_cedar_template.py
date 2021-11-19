import json
import requests
import configparser
from properties import create_field, create_template, create_element

# TODO options: config, data, template name, template description
# TODO add schema:identifier
# TODO make sure required works

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['cedar']['key']
# folder = config['cedar']['folder']
folder = None

data = [
    {
        'name': 'BioSample',
        'description': 'Data about a physical sample consisting of one or more cells taken from an organism (living or deceased) or derived from such a Sample.',
        'identifier': 'https://datamodel.terra.bio/TerraCore#BioSample',
        'fields': [
            {
                'name': 'donated',
                'description': 'Whether or not it was donated',
                'identifier': 'https://datamodel.terra.bio/TerraCore#donated'
            },
            {
                'name': 'hasBioSampleType',
                'description': 'Has a bio sample type',
                'identifier': 'https://datamodel.terra.bio/TerraCore#hasBioSampleType'
            },
            {
                'name': 'wasUsedBy',
                'description': 'Was used by',
                'identifier': 'https://datamodel.terra.bio/TerraCore#wasUsedBy'
            }
        ]
    },
    {
        'name': 'Dataset',
        'description': 'A set of data',
        'identifier': 'https://datamodel.terra.bio/TerraCore#Dataset',
        'fields': [
            {
                'name': 'hasDataUseLimitation',
                'description': 'Has a limitation on data use',
                'identifier': 'https://datamodel.terra.bio/TerraCore#hasDataUseLimitation'
            },
            {
                'name': 'hasDataUseRequirement',
                'description': 'Has a requirement for data use',
                'identifier': 'https://datamodel.terra.bio/TerraCore#hasDataUseRequirement'
            }
        ]
    }
]

base_rest_url = 'https://resource.metadatacenter.org'
field_validator_endpoint = '/command/validate?resource_type=field'
element_validator_endpoint = '/command/validate?resource_type=element'
template_validator_endpoint = '/command/validate?resource_type=template'
templates_endpoint = '/templates'
template_fields_endpoint = '/template-fields'
template_elements_endpoint = '/template-elements'


def post_request(endpoint, property):
    headers = {
        'Authorization': 'apiKey {0}'.format(api_key),
        'Accept': 'application/json'
    }
    return requests.post(base_rest_url +
                         endpoint, data=json.dumps(property), params={'folder_id': folder}, headers=headers)


def validate(endpoint, property):
    response = post_request(endpoint, property)
    if response.status_code > 299:
        raise Exception('Validation error for {0}'.format(
            property['name']), response.text)
    print('{0} is a valid property'.format(property['schema:name']))


def add_child_to_parent(parent, child, identifier):
    name = child['schema:name']
    parent['properties'][name] = child
    parent['_ui']['order'].append(name)
    parent['_ui']['propertyLabels'][name] = name
    # TODO: shouldn't this be the description?
    parent['_ui']['propertyDescriptions'][name] = "Help Text"
    parent['properties']['@context']['properties'][name] = {
        "enum": [identifier]
    }
    # TODO: Make required for now
    parent['properties']['@context']['required'].append(name)
    parent['required'].append(name)


template_object = create_template('test-template', 'test-template-description')

field_objects = []
element_objects = []

# Validate fields and elements
for element in data:
    element_object = create_element(
        element['name'], element['description'], element['identifier'])
    for field in element['fields']:
        field_object = create_field(**field)
        validate(field_validator_endpoint, field_object)
        add_child_to_parent(element_object, field_object, field['identifier'])
        field_objects.append(field_object)
    validate(element_validator_endpoint, element_object)
    add_child_to_parent(template_object, element_object, element['identifier'])
    element_objects.append(element_object)

# Validate template
validate(template_validator_endpoint, template_object)

print('\n')

# Create fields
for field_object in field_objects:
    resp = post_request(template_fields_endpoint, field_object)
    if resp.status_code != 201:
        raise Exception('Creating field {0} failed'.format(
            field_object['schema:name']), resp.text)
    # Grab id from field so that element can use it
    field_object['@id'] = json.loads(resp.text)['@id']
    print('Field {0} created'.format(field_object['schema:name']))

# Create elements
for element_object in element_objects:
    resp = post_request(template_elements_endpoint, element_object)
    if resp.status_code != 201:
        raise Exception('Creating element {0} failed:'.format(
            element_object['schema:name']), resp.text)
    # Grab id from element so that template can use it
    element_object['@id'] = json.loads(resp.text)['@id']
    print('Element {0} created'.format(element_object['schema:name']))

# Create template
resp = post_request(templates_endpoint, template_object)
if resp.status_code != 201:
    raise Exception('Creating template failed:', resp.text)
print('\nCreated template!')
