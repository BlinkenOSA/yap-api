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
    types = serializers.SlugRelatedField(many=True, slug_field='type', read_only=True)
    genres = serializers.SlugRelatedField(many=True, slug_field='genre', read_only=True)
    languages = LanguageSerializer(many=True)
    spatial_coverage = CitySerializer(many=True)
    descriptions = serializers.SlugRelatedField(many=True, slug_field='description', read_only=True, source='record_descriptions')
    collectors = serializers.SlugRelatedField(many=True, slug_field='collector', read_only=True, source='record_collectors')
    creators = serializers.SlugRelatedField(many=True, slug_field='creator', read_only=True, source='record_creators')
    subjects = serializers.SlugRelatedField(many=True, slug_field='subject', read_only=True, source='record_subjects')
    subject_people = serializers.SlugRelatedField(many=True, slug_field='subject_person', read_only=True, source='record_subject_people')

    class Meta:
        model = Record
        exclude = ('preview',)
