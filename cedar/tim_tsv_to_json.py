# python3 tim_tsv_to_json.py <list of tsv files>

import sys
import json


element_definitions = {
    'Dataset': 'An extension of DCAT:Dataset to support Data Use Ontology terms. A collection of one or more entities submitted by a single responsible party or authorizing agent.',
    'Project': 'A collective effort with an objective related to biomedical research.',
    'BioSample': 'Data about a physical sample consisting of one or more cells taken from an organism (living or deceased) or derived from such a Sample.',
    'Donor': 'An organism from which a sample or test result is available.'
}

elements = []

for i in range(1, len(sys.argv)):
    f = sys.argv[i]
    name = f.replace('.tsv', '')
    el = {
        'name': name,
        'description': element_definitions[name],
        'identifier': 'https://datamodel.terra.bio/TerraCore#{0}'.format(name),
        'fields': []
    }
    for line in open(f).read().splitlines():
        # The data is a bit messy...
        values = line.split('\t')
        property = values[0]
        if len(values) > 3:
            definition = values[3]
        else:
            definition = ""
        try:
            name = property.split(':')[1]
        except:
            name = property
        if property.startswith('TerraCore'):
            property = 'https://datamodel.terra.bio/TerraCore#{0}'.format(name)
        el['fields'].append({
            'name': name.strip(),
            'description': definition.strip(),
            'identifier': property.strip()
        })
    elements.append(el)

with open('tim.json', 'w') as fp:
    json.dump({'tim': elements}, fp)
