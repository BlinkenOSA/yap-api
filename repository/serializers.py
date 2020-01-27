from rest_framework import serializers

from repository.models import Record, Language, City, Collection


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ('id',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ('id',)


class CollectionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    record_count = serializers.SerializerMethodField()

    def get_record_count(self, obj):
        return obj.record_set.count()

    class Meta:
        model = Collection
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    collection = CollectionSerializer(read_only=True)
    type = serializers.SlugRelatedField(many=True, slug_field='type', read_only=True, source='types')
    genre = serializers.SlugRelatedField(many=True, slug_field='genre', read_only=True, source='genres')
    archival_reference_number = serializers.SerializerMethodField()
    date_of_creation_start = serializers.CharField(source='creation_date_start')
    date_of_creation_end = serializers.CharField(source='creation_date_end')
    language = LanguageSerializer(many=True, source='languages')
    city = CitySerializer(many=True, source='spatial_coverage')
    description = serializers.SlugRelatedField(many=True, slug_field='description', read_only=True, source='record_descriptions')
    collector = serializers.SlugRelatedField(many=True, slug_field='collector', read_only=True, source='record_collectors')
    creator = serializers.SlugRelatedField(many=True, slug_field='creator', read_only=True, source='record_creators')
    subject = serializers.SlugRelatedField(many=True, slug_field='subject', read_only=True, source='record_subjects')
    subject_people = serializers.SlugRelatedField(many=True, slug_field='subject_person', read_only=True, source='record_subject_people')
    thumbnails = serializers.SlugRelatedField(many=True, slug_field='thumbnail', read_only=True, source='record_thumbnails')
    media_files = serializers.SlugRelatedField(many=True, slug_field='file', read_only=True, source='record_media_files')

    def get_archival_reference_number(self, obj):
        return "HU OSA %s-%s-%s:%s/%s" % (obj.fonds, obj.subfonds, obj.series, obj.container_no, obj.sequence_no)

    class Meta:
        model = Record
        fields = ['id', 'collection', 'archival_reference_number', 'fonds', 'subfonds', 'series', 'container_no', 'sequence_no',
                  'title_original', 'title_english', 'date_of_creation_start', 'date_of_creation_end',
                  'extent', 'description_level', 'description',
                  'temporal_coverage_start', 'temporal_coverage_end',
                  'type', 'genre', 'language', 'city',
                  'collector', 'creator', 'subject', 'subject_people',
                  'privacy', 'thumbnails', 'media_files']
