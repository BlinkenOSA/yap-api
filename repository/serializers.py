from rest_framework import serializers

from repository.models import Record, Type, Genre, Language, City, RecordCreator, RecordCollector


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ('id',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ('id',)


class RecordSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    type = serializers.SlugRelatedField(many=True, slug_field='type', read_only=True, source='types')
    genre = serializers.SlugRelatedField(many=True, slug_field='genre', read_only=True, source='genres')
    language = LanguageSerializer(many=True, source='language')
    city = CitySerializer(many=True, source='spatial_coverage')
    description = serializers.SlugRelatedField(many=True, slug_field='description', read_only=True, source='record_descriptions')
    collector = serializers.SlugRelatedField(many=True, slug_field='collector', read_only=True, source='record_collectors')
    creator = serializers.SlugRelatedField(many=True, slug_field='creator', read_only=True, source='record_creators')
    subject = serializers.SlugRelatedField(many=True, slug_field='subject', read_only=True, source='record_subjects')
    subject_people = serializers.SlugRelatedField(many=True, slug_field='subject_person', read_only=True, source='record_subject_people')

    class Meta:
        model = Record
        include = ['id', 'fonds', 'subfonds', 'series', 'container_no', 'sequence_no',
                   'title_original', 'title_english', 'creation_date_start', 'creation_date_end',
                   'extent', 'description_level', 'description',
                   'temporal_coverage_start', 'temporal_coverage_end',
                   'type', 'genre', 'language', 'city',
                   'collector', 'creator', 'subject', 'subject_people',
                   'privacy']
