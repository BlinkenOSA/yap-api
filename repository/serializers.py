from rest_framework import serializers

from repository.models import Record, Type, Genre, Language


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True)
    genres = GenreSerializer(many=True)
    languages = LanguageSerializer(many=True)
    spatial_coverage = CitySerializer(many=True)

    class Meta:
        model = Record
        exclude = ('preview',)
