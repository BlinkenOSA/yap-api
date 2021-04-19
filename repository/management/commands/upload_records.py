import csv
import os

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django_date_extensions.fields import ApproximateDate

from repository.models import Record, RecordCreator, Type, Genre, Language, RecordDescription, RecordSubject, \
    RecordSubjectPerson, City, RecordCollector, Collection


class Command(BaseCommand):
    help = 'Import records from csv files.'

    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds number.', default=None)
        parser.add_argument('--subfonds', dest='subfonds', help='Subfonds number.', default=0)
        parser.add_argument('--series', dest='series', help='Series number.', default=0)
        parser.add_argument('--collection', dest='collection', help='Collection ID', default=None)
        parser.add_argument('--delete', dest='delete', help='Delete the existing ones', default=False)

    def handle(self, *args, **options):
        fonds = options.get('fonds', 0)
        subfonds = options.get('subfonds', 0)
        series = options.get('series', 0)
        delete = options.get('delete', False)

        collection_id = options.get('collection', 'HU OSA')
        collection = Collection.objects.get(archival_reference_code=collection_id)

        if delete:
            Record.objects.filter(collection=collection).delete()

        with open(os.path.join(os.getcwd(), 'import', 'HU OSA %s-%s-%s.csv' % (fonds, subfonds, series)), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["FondsID"] != '':
                    record, created = Record.objects.get_or_create(
                        fonds=int(row['FondsID']),
                        subfonds=int(row['SubfondsID'] if row['SubfondsID'] else None),
                        series=int(row['SeriesID'] if row['SeriesID'] else None),
                        container_no=int(row['Container']),
                        sequence_no=int(row['No']),
                        collection=collection
                    )

                    record.title_original = row['Title Original']
                    record.title_english = row['Title English']

                    if row['Date of Creation (YYYY)'] != '':
                        record.creation_date_start = self.make_date(row['Date of Creation (YYYY)'],
                                                                    row['Date of Creation (MM)'],
                                                                    row['Date of Creation (DD)'])

                    if row['Date of Creation2 (YYYY)'] != '':
                        record.creation_date_end = self.make_date(row['Date of Creation2 (YYYY)'],
                                                                  row['Date of Creation2 (MM)'],
                                                                  row['Date of Creation2 (DD)'])

                    record.extent = row['Extent']
                    if row['Description Level'] == 'Folder':
                        record.description_level = 'F'
                    else:
                        record.description_level = 'I'

                    if row['Temporal Coverage1 (YYYY)'] != '':
                        record.temporal_coverage_start = int(row['Temporal Coverage1 (YYYY)'])

                    if row['Temporal Coverage2 (YYYY)'] != '':
                        record.temporal_coverage_end = int(row['Temporal Coverage2 (YYYY)'])

                    record.privacy = row['Privacy/Access']
                    record.internal_note = row['Internal Note']
                    record.preview = row['Preview']

                    # Collectors
                    collector, created = RecordCollector.objects.get_or_create(
                        record=record,
                        collector=row['Collector'].strip()
                    )

                    # Types
                    type, created = Type.objects.get_or_create(
                        type=row['Type'].strip()
                    )
                    record.types.add(type)

                    # Genres
                    for genre in row['Genre'].split("|"):
                        if genre != '':
                            g, created = Genre.objects.get_or_create(genre=genre.strip())
                            record.genres.add(g)

                    # Languages
                    for language in row['Language'].split("|"):
                        if language != '':
                            l, created = Language.objects.get_or_create(language=language.strip())
                            record.languages.add(l)

                    # Creators
                    for creator in row['Creator'].split("|"):
                        if creator != '':
                            RecordCreator.objects.get_or_create(record=record, creator=creator.strip())

                    # Description
                    for description in row['Description/Annotation/Abstract'].split("|"):
                        if description != '':
                            RecordDescription.objects.get_or_create(record=record, description=description.strip())

                    # Subject
                    for subject in row['Subject (Event, Topic, Corporate body, Location outside of YU)'].split("|"):
                        if subject != '':
                            RecordSubject.objects.get_or_create(record=record, subject=subject.strip())

                    # Subject Person
                    for subject_person in row['Subject (Person)'].split("|"):
                        if subject_person != '':
                            RecordSubjectPerson.objects.get_or_create(record=record, subject_person=subject_person.strip())

                    print("Adding record: HU OSA %s-%s-%s:%s/%s" % (row['FondsID'], row['SubfondsID'], row['SeriesID'], row['Container'], row['No']))

                if row['Geo Coordinates'] != '':
                    # Spatial Coverage
                    city, created = City.objects.get_or_create(city=row['Spatial Coverage3'])
                    geo = row['Geo Coordinates'].split(",")
                    city.latitude = float(geo[0])
                    city.longitude = float(geo[1])
                    city.save()

                    record.spatial_coverage.add(city)
                    print("Adding city: %s to record" % city.city)

                try:
                    record.save()
                except ValueError as e:
                    print(e)
                except ValidationError as e:
                    print(e)

    def make_date(self, year, month, day):
        try:
            if month:
                if day:
                    date = "%s-%02d-%02d" % (int(year), int(month), int(day))
                    ApproximateDate(year=int(year), month=int(month), day=int(day))
                else:
                    date = "%s-%02d-00" % (int(year), int(month))
                    ApproximateDate(year=int(year), month=int(month))
            else:
                date = "%s-00-00" % year
                ApproximateDate(year=int(year))
            return date

        except ValueError:
            print('Invalid date!')
            return None

