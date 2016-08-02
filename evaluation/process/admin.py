from django.contrib import admin
from .models import Process
from .models import ProcessQueue
from .models import ProcessQueueItem
from .models import Algorithm
from .models import Job
from .models import JobStep


class ProcessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Process, ProcessAdmin)


class ProcessQueueItemAdmin(admin.TabularInline):
    model = ProcessQueueItem


class ProcessQueueAdmin(admin.ModelAdmin):
    inlines = [ProcessQueueItemAdmin,]

admin.site.register(ProcessQueue, ProcessQueueAdmin)


class AlgorithmAdmin(admin.ModelAdmin):
    pass

admin.site.register(Algorithm, AlgorithmAdmin)


class JobStepAdmin(admin.TabularInline):
    model = JobStep


class JobAdmin(admin.ModelAdmin):
    inlines = [JobStepAdmin,]

admin.site.register(Job, JobAdmin)