from django.core.management import BaseCommand
from repository.models import Record, Collection


class Command(BaseCommand):
    help = 'Index records.'

    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds number.', default=None)
        parser.add_argument('--subfonds', dest='subfonds', help='Subfonds number.', default=None)
        parser.add_argument('--series', dest='series', help='Series number.', default=None)
        parser.add_argument('--collection', dest='collection', help='Collection ID.', default=None)

    def handle(self, *args, **options):
        fonds = options.get('fonds', 0)
        subfonds = options.get('subfonds', 0)
        series = options.get('series', 0)

        records = Record.objects.filter(fonds=fonds, subfonds=subfonds, series=series).iterator()
        collection = Collection.objects.get(pk=options.get('collection'))

        for record in records:
            record.collection = collection
            print('Saving record: %s' % record.id)
            record.save()