from django.contrib import admin

from .models import CSVFile, Participant, Tag, Evidence


@admin.register(CSVFile)
class CSVAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    # readonly_fields: ('get_evidence', )

    # @admin.display(description='pEvidence')
    # def get_evidence(self, obj):
    #     return [e.text for e in Evidence.objects.get(participant=obj.id)]

    list_display = ('name', 'role', 'industry', 'orgSize')


    fieldsets = (
        ('Info', {
            'fields': (('name', 'role'), ('industry', 'orgSize')),
            'classes': ('collapse', 'pretty')
        }),
        ('Evidence', {
            'fields': [],
            'classes': ('collapse', 'pretty')
        })
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
