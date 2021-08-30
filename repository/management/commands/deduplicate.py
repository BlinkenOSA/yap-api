from django.core.management import BaseCommand
from django.db.models import Q, Count

from repository.models import Record, City, Genre, Type


class Command(BaseCommand):
    help = 'Deduplicate entries.'

    def handle(self, *args, **options):
        # Remove spaces from the city names
        self.strip_fields(City, 'city')

        # Remove spaces from the genre names
        self.strip_fields(Genre, 'genre')

        # Remove spaces from the type names
        self.strip_fields(Type, 'type')

        # Reassign and elminate duplicated cities
        duplicate_cities = City.objects.values('city').annotate(city_count=Count('city')).filter(city_count__gt=1)
        for data in duplicate_cities:
            print("Find duplicated city: %s" % data['city'])
            original = City.objects.filter(city=data['city']).first()
            duplications = City.objects.filter(city=data['city']).exclude(pk=original.id)
            for duplication in duplications:
                for report in Record.objects.filter(spatial_coverage__id=duplication.id).iterator():
                    print(
                        "Reassign city in report HU %s-%s-%s:%s/%s" %
                        (report.fonds, report.subfonds, report.series, report.container_no, report.sequence_no)
                    )
                    report.spatial_coverage.remove(duplication)
                    report.spatial_coverage.add(original)
                duplication.delete()

        # Reassign and elminate duplicated genres
        duplicate_genres = Genre.objects.values('genre').annotate(genre_count=Count('genre')).filter(genre_count__gt=1)
        for data in duplicate_genres:
            print("Find duplicated genre: %s" % data['genre'])
            original = Genre.objects.filter(genre=data['genre']).first()
            duplications = Genre.objects.filter(genre=data['genre']).exclude(pk=original.id)
            for duplication in duplications:
                for report in Record.objects.filter(genres__id=duplication.id).iterator():
                    print(
                        "Reassign genre in report HU %s-%s-%s:%s/%s" %
                        (report.fonds, report.subfonds, report.series, report.container_no, report.sequence_no)
                    )
                    report.genres.remove(duplication)
                    report.genres.add(original)
                duplication.delete()

        # Reassign and elminate duplicated types
        duplicate_types = Type.objects.values('type').annotate(type_count=Count('type')).filter(type_count__gt=1)
        for data in duplicate_types:
            print("Find duplicated type: %s" % data['type'])
            original = Type.objects.filter(type=data['type']).first()
            duplications = Type.objects.filter(type=data['type']).exclude(pk=original.id)
            for duplication in duplications:
                for report in Record.objects.filter(types__id=duplication.id).iterator():
                    print(
                        "Reassign type in report HU %s-%s-%s:%s/%s" %
                        (report.fonds, report.subfonds, report.series, report.container_no, report.sequence_no)
                    )
                    report.types.remove(duplication)
                    report.types.add(original)
                duplication.delete()

    def strip_fields(self, model, field):
        for record in model.objects.iterator():
            setattr(record, field, getattr(record, field).strip())
            record.save()
