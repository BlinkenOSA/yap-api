# Generated by Django 2.2.7 on 2020-01-27 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_collection_archival_reference_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordThumbnail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('thumbnail', models.CharField(blank=True, max_length=200, null=True, verbose_name='Thumbnail')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_thumbnails', to='repository.Record')),
            ],
            options={
                'verbose_name': 'thumbnail',
                'verbose_name_plural': 'thumbnails',
                'db_table': 'record_thumbnails',
            },
        ),
        migrations.CreateModel(
            name='RecordMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.CharField(blank=True, max_length=200, null=True, verbose_name='Media File')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_media_files', to='repository.Record')),
            ],
            options={
                'verbose_name': 'media file',
                'verbose_name_plural': 'media files',
                'db_table': 'record_media_files',
            },
        ),
    ]
