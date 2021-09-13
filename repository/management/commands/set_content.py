import requests

from django.core.management import BaseCommand
from repository.models import Record, RecordMedia, RecordThumbnail


class Command(BaseCommand):
    help = 'Set content if exists.'

    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds number.', default=None)

    def handle(self, *args, **options):
        fonds = options.get('fonds', 0)

        for record in Record.objects.filter(fonds=fonds).iterator():
            filename = 'hu_osa_%s-%s-%s_%s_%s' % (record.fonds, record.subfonds, record.series,
                                                  record.container_no, record.sequence_no)

            mp4_file = 'https://storage.osaarchivum.org/yap/video/%s.mp4' % filename
            response = requests.head(mp4_file)
            if response.status_code == 200:
                if RecordMedia.objects.filter(file=mp4_file).count() == 0:
                    RecordMedia.objects.create(
                        record=record,
                        file=mp4_file,
                        mimetype='video/mp4'
                    )
                    print("Added thumbnail: %s" % mp4_file)
                record.save()
            else:
                print("No record exists for: %s" % mp4_file)

            thumbnail_file = 'https://storage.osaarchivum.org/yap/thumbnail/%s.jpg' % filename
            response = requests.head(thumbnail_file)
            if response.status_code == 200:
                if RecordThumbnail.objects.filter(thumbnail=thumbnail_file).count() == 0:
                    RecordThumbnail.objects.create(
                        record=record,
                        thumbnail=thumbnail_file,
                        mimetype='image/jpeg'
                    )
                    print("Added mp4: %s" % thumbnail_file)
                record.save()
            else:
                print("No record exists for: %s" % thumbnail_file)