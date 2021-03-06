from django.contrib import admin
from .models import ProcessResult, SizeIndexThresholdLog, CropToCenterLog


class SizeIndexLogAdmin(admin.TabularInline):
    model = SizeIndexThresholdLog


class CropToCenterLogAdmin(admin.TabularInline):
    model = CropToCenterLog


class ProcessResultAdmin(admin.ModelAdmin):
    inlines = [SizeIndexLogAdmin, CropToCenterLogAdmin,]
    list_filter = ['evaluation__region_isolate', 'source', 'evaluation__border_quality', 'category',]
    list_display = ('name', 'source', 'SFA_major', 'SFA_minor', 'color_score', 'border')

admin.site.register(ProcessResult, ProcessResultAdmin)