from django.db import models
from django_date_extensions.fields import ApproximateDateField


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='Title', max_length=500)
    year_start = models.IntegerField(verbose_name='Year Start', blank=True, null=True)
    year_end = models.IntegerField(verbose_name='Year End', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    archival_reference_code = models.CharField(verbose_name='Archival Reference Code', max_length=100, blank=True, null=True)
    catalog_url = models.CharField(verbose_name='Catalog URL', max_length=500, blank=True, null=True)
    thumbnail = models.CharField(verbose_name='Thumbnail', max_length=200, blank=True, null=True)
    sort_index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.archival_reference_code, self.title)

    class Meta:
        db_table = 'collections'
        verbose_name = 'collection'
        verbose_name_plural = 'collections'


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='Collection')

    # Archival Identifiers
    fonds = models.IntegerField(verbose_name='Fonds')
    subfonds = models.IntegerField(verbose_name='Subfonds')
    series = models.IntegerField(verbose_name='Series')
    container_no = models.IntegerField(verbose_name='Container Number')
    sequence_no = models.IntegerField(verbose_name='Sequence Number')

    # Metadata
    title_original = models.CharField(verbose_name='Original Title', max_length=500)
    title_english = models.CharField(verbose_name='English Title', max_length=500, blank=True, null=True)
    creation_date_start = ApproximateDateField(verbose_name='Date of Creation (Start)')
    creation_date_end = ApproximateDateField(verbose_name='Date of Creation (End)', blank=True, null=True)

    types = models.ManyToManyField('Type', verbose_name='Type', blank=True)
    genres = models.ManyToManyField('Genre', verbose_name='Genre', blank=True)
    languages = models.ManyToManyField('Language', verbose_name='Language', blank=True)

    extent = models.CharField(verbose_name='Extent', max_length=50, blank=True, null=True)
    DESCRIPTION_LEVEL = [('F', 'Folder'), ('I', 'Item')]
    description_level = models.CharField(max_length=2, choices=DESCRIPTION_LEVEL, default='F')

    temporal_coverage_start = models.IntegerField(verbose_name='Temporal Coverage (Start)', blank=True, null=True)
    temporal_coverage_end = models.IntegerField(verbose_name='Temporal Coverage (End)', blank=True, null=True)

    spatial_coverage = models.ManyToManyField('City', verbose_name='Spatial Coverage', blank=True)

    privacy = models.TextField(verbose_name='Privacy / Access', blank=True)
    internal_note = models.TextField(verbose_name='Internal Note', blank=True)
    preview = models.CharField(verbose_name='Preview', max_length=200, blank=True, null=True)
    catalog_url = models.CharField(verbose_name='Catalog URL', max_length=500, blank=True, null=True)

    def __str__(self):
        return "HU OSA %s-%s-%s/%s:%s" % (self.fonds, self.subfonds, self.series, self.container_no, self.sequence_no)

    class Meta:
        db_table = 'records'
        verbose_name = 'record'
        verbose_name_plural = 'records'


class RecordMedia(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_media_files')
    file = models.CharField(verbose_name='Media File', max_length=200, blank=True, null=True)
    mimetype = models.CharField(verbose_name='Media File MIME Type', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'record_media_files'
        verbose_name = 'media file'
        verbose_name_plural = 'media files'


class RecordThumbnail(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_thumbnails')
    thumbnail = models.CharField(verbose_name='Thumbnail', max_length=200, blank=True, null=True)
    mimetype = models.CharField(verbose_name='Media File MIME Type', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'record_thumbnails'
        verbose_name = 'thumbnail'
        verbose_name_plural = 'thumbnails'


class RecordCreator(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_creators')
    creator = models.CharField(verbose_name='Creator', max_length=500)

    class Meta:
        db_table = 'record_creators'
        verbose_name = 'creator'
        verbose_name_plural = 'creators'


class RecordDescription(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_descriptions')
    description = models.TextField(verbose_name='Description')

    class Meta:
        db_table = 'record_descriptions'
        verbose_name = 'description'
        verbose_name_plural = 'descriptions'


class RecordCollector(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_collectors')
    collector = models.CharField(verbose_name='Collector', max_length=300)

    class Meta:
        db_table = 'record_collectors'
        verbose_name = 'collector'
        verbose_name_plural = 'collectors'


class RecordSubject(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_subjects')
    subject = models.CharField(verbose_name='Subject', max_length=200)

    class Meta:
        db_table = 'record_subjects'
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'


class RecordSubjectPerson(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='record_subject_people')
    subject_person = models.CharField(verbose_name='Subject (Person)', max_length=300)

    class Meta:
        db_table = 'record_subject_people'
        verbose_name = 'subject person'
        verbose_name_plural = 'subject people'


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(verbose_name='Type', max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'types'
        verbose_name = 'type'
        verbose_name_plural = 'types'
        ordering = ['type']


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(verbose_name='Genre', max_length=50)

    def __str__(self):
        return self.genre

    class Meta:
        db_table = 'genres'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['genre']


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(verbose_name='Language', max_length=100)
    iso_639_1 = models.CharField(verbose_name='ISO 639-1', max_length=10, blank=True, null=True)
    iso_639_2 = models.CharField(verbose_name='ISO 639-2', max_length=10, blank=True, null=True)

    def __str__(self):
        return self.language

    class Meta:
        db_table = 'languages'
        verbose_name = 'language'
        verbose_name_plural = 'languages'
        ordering = ['language']


class City(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(verbose_name='City', max_length=50)
    latitude = models.FloatField(verbose_name='Latitude', blank=True, null=True)
    longitude = models.FloatField(verbose_name='Longitude', blank=True, null=True)

    def __str__(self):
        return self.city

    class Meta:
        db_table = 'cities'
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        ordering = ['city']
