from django.core.management import BaseCommand

from repository.record_indexer import RecordIndexer
from repository.models import Record


class Command(BaseCommand):
    help = 'Index records.'

    def handle(self, *args, **options):
        for record in Record.objects.all().iterator():
            indexer = RecordIndexer(record)
            indexer.index()
