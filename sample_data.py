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
