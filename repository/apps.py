from django.apps import AppConfig


class RepositoryConfig(AppConfig):
    name = 'repository'

    def ready(self):
        super(RepositoryConfig, self).ready()
        from repository.signals import update_record_index
