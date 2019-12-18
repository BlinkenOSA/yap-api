import re

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from pysolr import SolrError
from rest_framework import generics
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from repository.inspectors.record_search_inspector import RecordSearchInspector
from repository.models import Record
from repository.serializers import RecordSerializer
from yap_api.searcher import Searcher


class RecordDetail(generics.RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class RecordFilterClass(filters.FilterSet):
    cursorMark = filters.CharFilter(label='Cursor')
    query = filters.CharFilter(label='Search')
    ordering = OrderingFilter(fields=(('score', 'score'),))

    record_origin = filters.CharFilter(label='Record Origin')
    description_level = filters.CharFilter(label='Description Level')
    language = filters.CharFilter(label='Language')
    city = filters.CharFilter(label='City')
    creator = filters.CharFilter(label='Creator')
    collector = filters.CharFilter(label='Collector')
    collection = filters.CharFilter(label='Collection')
    genre = filters.CharFilter(label='Genre')
    type = filters.CharFilter(label='Type')
    subject = filters.CharFilter(label='Subject')
    subject_person = filters.CharFilter(label='Subject (Person)')

    year_coverage_start = filters.NumberFilter(label='Coverage year (Start)')
    year_coverage_end = filters.NumberFilter(label='Coverage year (End)')

    geo_bottom_left = filters.CharFilter(label='Map bounding box (Bottom left corner)')
    geo_top_right = filters.CharFilter(label='Map bounding box (Top right corner)')


@method_decorator(name='get', decorator=swagger_auto_schema(
   filter_inspectors=[RecordSearchInspector]
))
class RecordList(ListAPIView):
    queryset = Record.objects.all()
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RecordFilterClass
    core = "yap"

    def list(self, request, *args, **kwargs):
        filters = []
        date_filters = []
        cursor_mark = request.query_params.get('cursorMark', '*')

        qf = [
            'title_original_search^5.0',
            'title_english_search^5.0',
            'description_search^2.5',
            'subject_search^2.5',
            'subject_person_search^1.5',
            'city_search^1.5'
        ]

        # Facets
        filters = self._set_filter(request, 'record_origin', filters)
        filters = self._set_filter(request, 'description_level', filters)
        filters = self._set_filter(request, 'language', filters)
        filters = self._set_filter(request, 'city', filters)
        filters = self._set_filter(request, 'creator', filters)
        filters = self._set_filter(request, 'collector', filters)
        filters = self._set_filter(request, 'collection', filters)
        filters = self._set_filter(request, 'genre', filters)
        filters = self._set_filter(request, 'type', filters)
        filters = self._set_filter(request, 'subject', filters)
        filters = self._set_filter(request, 'subject_person', filters)

        year_from = request.query_params.get('year_coverage_start', None)
        year_to = request.query_params.get('year_coverage_to', None)

        # Date coverage
        try:
            if year_from:
                if re.match(r'.*([1-3][0-9]{3})', year_from):
                    date_filters.append({'year_coverage_start': '[* TO %s]' % year_from})
            if year_to:
                if re.match(r'.*([1-3][0-9]{3})', year_to):
                    date_filters.append({'year_coverage_to': '[%s TO *]' % year_to})
        except ValueError:
            pass

        # GEO Filters
        geo_bottom_left = request.query_params.get('geo_bottom_left', None)
        geo_top_right = request.query_params.get('geo_top_right', None)
        if geo_bottom_left and geo_top_right:
            date_filters.append({'geo_search': '[%s TO %s]' % (geo_bottom_left, geo_top_right)})

        params = {
            'search': request.query_params.get('query', ''),
            'ordering': request.query_params.get('ordering', '-score'),
            'qf': qf,
            'fl': 'id,archival_reference_number,title_original,title_english,'
                  'date_of_creation_start,date_of_creation_end,'
                  'temporal_coverage_start,temporal_coverage_end,'
                  'description,genre,type,city,',
            'facet': True,
            'facet_fields': [
                'record_origin_facet', 'description_level_facet', 'language_facet',
                'city_facet', 'creator_facet', 'collector_facet',
                'collection_facet', 'genre_facet',
                'type_facet', 'subject_facet', 'subject_person_facet'
            ],
            'facet_sort': 'count',
            'filters': filters,
            'date_filters': date_filters
        }

        searcher = Searcher(self.core)
        searcher.initialize(params, tie_breaker='id asc')

        try:
            response = searcher.search(cursor_mark=cursor_mark)
        except SolrError as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(e)})

        resp = {
            'count': response.hits,
            'results': response.docs,
            'facets': response.facets,
            'nextCursorMark': response.nextCursorMark
        }

        return Response(resp)

    def _set_filter(self, request, field_name, filters):
        f_param = request.query_params.get(field_name, None)
        if f_param:
            filters.append({'%s_facet' % field_name: f_param})
        return filters
