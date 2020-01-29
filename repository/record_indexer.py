import pysolr
from django.conf import settings


class RecordIndexer:
    """
    Class to index Repository record records to Solr.
    """

    def __init__(self, record):
        self.record = record
        self.solr_core = getattr(settings, "SOLR_CORE", "yap")
        self.solr_url = "%s/%s" % (getattr(settings, "SOLR_URL", "http://localhost:8983/solr"), self.solr_core)
        self.solr = pysolr.Solr(self.solr_url)
        self.doc = {
            # Display fields
            'id': None,
            'description': [],
            'genre': [],
            'type': [],
            'city': [],
            'thumbnails': [],

            # Search fields
            'description_search': [],
            'subject_search': [],
            'subject_person_search': [],
            'city_search': [],
            'geo_search': [],

            # Facet fields
            'language_facet': [],
            'city_facet': [],
            'creator_facet': [],
            'collector_facet': [],
            'genre_facet': [],
            'type_facet': [],
            'subject_facet': [],
            'subject_person_facet': []
        }

    def index(self):
        self._index_record()
        try:
            self.solr.add([self.doc], commit=True)
            print('Indexed record no. %s!' % self.doc['id'])
        except pysolr.SolrError as e:
            print('Error with record no. %s! Error: %s' % (self.doc['id'], e))

    def _index_record(self):
        self.doc['id'] = self.record.id
        self.doc['archival_reference_number'] = "HU OSA %s-%s-%s:%s/%s" % (self.record.fonds,
                                                                           self.record.subfonds,
                                                                           self.record.series,
                                                                           self.record.container_no,
                                                                           self.record.sequence_no)
        if self.record.collection:
            self.doc['collection_title'] = self.record.collection.title
            self.doc['collection_archival_reference_code'] = self.record.collection.archival_reference_code
        self.doc['title_original'] = self.record.title_original
        self.doc['title_english'] = self.record.title_english
        self.doc['date_of_creation_start'] = str(self.record.creation_date_start)
        self.doc['date_of_creation_end'] = str(self.record.creation_date_end)
        self.doc['temporal_coverage_start'] = self.record.temporal_coverage_start
        self.doc['temporal_coverage_end'] = self.record.temporal_coverage_end

        for thumbnail in self.record.record_thumbnails.all():
            self.doc['thumbnails'].append(thumbnail.thumbnail)

        for description in self.record.record_descriptions.all():
            self.doc['description'].append(description.description)

        for genre in self.record.genres.all():
            self.doc['genre'].append(genre.genre)

        for type in self.record.types.all():
            self.doc['type'].append(type.type)

        for city in self.record.spatial_coverage.all():
            self.doc['city'].append(city.city)
            if city.latitude and city.longitude:
                self.doc['geo_search'].append("%s,%s" % (city.latitude, city.longitude))

        # Sort
        self.doc['archival_reference_number_sort'] = "%04d%04d%04d%04d%04d" % (self.record.fonds,
                                                                               self.record.subfonds,
                                                                               self.record.series,
                                                                               self.record.container_no,
                                                                               self.record.sequence_no)
        self.doc['title_english_sort'] = self.doc['title_english']
        self.doc['coverage_start_sort'] = self.record.temporal_coverage_start

        self.doc['title_original_search'] = self.doc['title_original']
        self.doc['title_english_search'] = self.doc['title_english']
        self.doc['description_search'] = self.doc['description']
        self.doc['city_search'] = self.doc['city']

        for subject in self.record.record_subjects.all():
            self.doc['subject_search'] = subject.subject

        for subject in self.record.record_subject_people.all():
            self.doc['subject_person_search'] = subject.subject_person

        self.doc['year_coverage_start'] = self.record.temporal_coverage_start
        self.doc['year_coverage_end'] = self.record.temporal_coverage_end

        if self.record.collection:
            self.doc['collection_facet'] = self.doc['collection_title']

        self.doc['genre_facet'] = self.doc['genre']
        self.doc['type_facet'] = self.doc['type']
        self.doc['city_facet'] = self.doc['city']
        self.doc['subject_facet'] = self.doc['subject_search']
        self.doc['subject_person_facet'] = self.doc['subject_person_search']

        for creator in self.record.record_creators.all():
            self.doc['creator_facet'].append(creator.creator)

        for collector in self.record.record_collectors.all():
            self.doc['collector_facet'].append(collector.collector)