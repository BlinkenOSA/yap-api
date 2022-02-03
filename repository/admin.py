from django.db import models
from django.contrib import admin
from django.forms import TextInput

from repository.models import Record, RecordThumbnail, RecordMedia, RecordDescription, City, Collection, RecordSubject, \
    RecordSubjectPerson, RecordCreator, RecordCollector, Type, Genre


class RecordSubjectInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordSubject
    extra = 1


class RecordSubjectPersonInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordSubjectPerson
    extra = 1


class RecordCreatorInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordCreator
    extra = 1


class RecordCollectorInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'class': 'tableText'})
        }
    }
    model = RecordCollector
    extra = 1


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
        RecordCreatorInline,
        RecordCollectorInline,
        RecordSubjectInline,
        RecordSubjectPersonInline
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
                'classes': ('placeholder record_creators-group',),
                'fields': ()
            }
        ), (
            '',
            {
                'classes': ('placeholder record_collectors-group',),
                'fields': ()
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
                'classes': ("placeholder record_subjects-group",),
                'fields': (),
            }
        ), (
            '',
            {
                'classes': ("placeholder record_subject_people-group",),
                'fields': (),
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
    list_display = ('title', 'description', 'catalog_url', 'thumbnail')
    list_editable = ('description', 'catalog_url', 'thumbnail')


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'latitude', 'longitude')
    list_editable = ('city', 'latitude', 'longitude')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_editable = ('type',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre')
    list_editable = ('genre',)


class RecordSubjectAdmin(admin.ModelAdmin):
    list_display = ('record', 'subject')
    list_editable = ('subject',)
    ordering = ('subject',)
    list_filter = ('subject',)


admin.site.register(Record, RecordAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(RecordSubject, RecordSubjectAdmin)
