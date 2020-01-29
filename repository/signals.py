from django.db.models.signals import post_save
from django.dispatch import receiver

from repository.models import Record
from repository.record_indexer import RecordIndexer


@receiver(post_save, sender=Record)
def update_record_index(sender, **kwargs):
    record = kwargs["instance"]
    indexer = RecordIndexer(record)
    indexer.index()
