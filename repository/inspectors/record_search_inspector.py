from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors import NotHandled, CoreAPICompatInspector


class RecordSearchInspector(CoreAPICompatInspector):
    fields = {
        'ordering': {
            'description': 'Definition of the resultset ordering.',
            'type': 'string',
            'enum': [
                'archival_reference_number_sort', '-archival_reference_number_sort',
                'title_english_sort', '-title_english_sort',
                'coverage_start_sort', '-coverage_start_sort',
                'score', '-score'
            ]
        },
        'cursorMark': {
            'description': 'Only submit it if there is a valid cursor in the response from Solr.',
            'type': 'string'
        },
        'query': {
            'description': 'Search string to search in the records.',
            'type': 'string'
        },
        'record_origin': {
            'description': 'Filter by record_origin',
            'type': 'string'
        },
        'description_level': {
            'description': 'Filter by description level',
            'type': 'string'
        },
        'language': {
            'description': 'Filter by language',
            'type': 'string'
        },
        'city': {
            'description': 'Filter by city',
            'type': 'string'
        },
        'creator': {
            'description': 'Filter by creator',
            'type': 'string'
        },
        'collector': {
            'description': 'Filter by collector',
            'type': 'string'
        },
        'collection': {
            'description': 'Filter by collection',
            'type': 'string'
        },
        'genre': {
            'description': 'Filter by genre',
            'type': 'string'
        },
        'type': {
            'description': 'Filter by type',
            'type': 'string'
        },
        'subject': {
            'description': 'Filter by subject',
            'type': 'string'
        },
        'subject_person': {
            'description': 'Filter by person (subject)',
            'type': 'string'
        },
        'year_coverage_start': {
            'description': 'Filter by temporal coverage (start)',
            'type': 'integer'
        },
        'year_coverage_end': {
            'description': 'Filter by temporal coverage (end)',
            'type': 'integer'
        },
        'geo_bottom_left': {
            'description': 'Map bounding box / Bottom left corner in a format of Lat,Long',
            'type': 'string'
        },
        'geo_top_right': {
            'description': 'Map bounding box / Top right corner in a format of Lat,Long',
            'type': 'string'
        },
    }

    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            results = super(RecordSearchInspector, self).get_filter_parameters(filter_backend)
            for param in results:
                for field, config in self.fields.items():
                    if param.get('name') == field:
                        if 'description' in config.keys():
                            param.description = config['description']
                        if 'type' in config.keys():
                            param.type = config['type']
                        if 'enum' in config.keys():
                            param.enum = config['enum']
            return results

        if isinstance(filter_backend, OrderingFilter):
            results = super(RecordSearchInspector, self).get_filter_parameters(filter_backend)
            return results

        return NotHandled