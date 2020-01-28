from django.db import models
from django.contrib import admin
from django.forms import TextInput

from repository.models import Record, RecordThumbnail, RecordMedia, RecordDescription, City, Collection


class RecordDescriptionInline(admin.TabularInline):
    formfield_overrides = {
        models.TextField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordDescription
    extra = 1


class RecordThumbnailInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordThumbnail
    extra = 1


class RecordMediaThumbnailInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordMedia
    extra = 1


class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ('fonds', 'subfonds', 'series')
    list_display = ('archival_reference_number', 'title_original', 'title_english')
    ordering = ('fonds', 'subfonds', 'series', 'container_no', 'sequence_no')
    list_filter = (
        ('collection', admin.RelatedOnlyFieldListFilter),
        ('fonds')
    )
    inlines = [
        RecordMediaThumbnailInline,
        RecordThumbnailInline,
        RecordDescriptionInline,
    ]
    search_fields = ['title_original', 'title_english', 'record_descriptions__description']
    preserve_filters = True
    filter_horizontal = ('types', 'genres', 'languages', 'spatial_coverage')
    fieldsets = (
        (
            '',
            {
                'fields': (('fonds', 'subfonds', 'series', 'container_no', 'sequence_no'), 'collection')
             }
        ), (
            '',
            {
                'classes': ('wide', ),
                'fields': (
                    'title_original', 'title_english',
                    ('creation_date_start', 'creation_date_end'),
                    'description_level', 'extent', 'catalog_url', 'internal_note'
                )
            }
        ), (
            '',
            {
                'fields': (('temporal_coverage_start', 'temporal_coverage_end'),)
            }
        ), (
            '',
            {
                'fields': ('types', 'genres', 'languages', 'spatial_coverage')
            }
        ), (
            '',
            {
                'classes': ('grp-collapse grp-closed placeholder record_descriptions-group',),
                'fields': ()
            }
        ), (
            '',
            {
                'classes': ("placeholder record_media_files-group",),
                'fields': (),
            }
        ), (
            '',
            {
                'classes': ("placeholder record_thumbnails-group",),
                'fields': (),
            }
        )
    )

    def archival_reference_number(self, obj):
        return "HU OSA %s-%s-%s/%s:%s" % (obj.fonds, obj.subfonds, obj.series, obj.container_no, obj.sequence_no)

    class Media:
        css = {
            'all': ('repository/css/styles.css',)
        }


class CollectionAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'latitude', 'longitude')
    list_editable = ('city', 'latitude', 'longitude')

admin.site.register(Record, RecordAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(City, CityAdmin)

