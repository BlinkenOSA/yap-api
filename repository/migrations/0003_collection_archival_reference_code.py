# Generated by Django 2.2.7 on 2020-01-16 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20200116_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='archival_reference_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Archival Reference Code'),
        ),
    ]