# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from border_results.models import ProcessResult as SourceImage


class ProcessQueue(models.Model):
    title = models.CharField(_("title"), max_length=255)

    class Meta:
        app_label = 'process'
        verbose_name = _('Process Queue')
        verbose_name_plural = _('Process Queues')


class Algorithm(models.Model):

    type = models.CharField(_('Algorithm Type'), max_length=255)

    class Meta:
        app_label = 'process'
        verbose_name = _('Algorithm')
        verbose_name_plural = _('Algorithms')


class Process(models.Model):

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), null=True, blank=True)
    type = models.ForeignKey(Algorithm, on_delete=models.SET_NULL, blank=True, null=True)
    parameters = models.TextField(_('Parameters'), null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.title)

    def get_absolute_url(self):
        return reverse('process:process-detail', args=[str(self.id)])

    class Meta:
        app_label = 'process'
        verbose_name = _('Process')
        verbose_name_plural = _('Processs')


class ProcessQueueItem(models.Model):
    queue = models.ForeignKey(ProcessQueue, related_name='+')
    process = models.ForeignKey(Process, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.IntegerField(_('Order'))

    def __unicode__(self):
        return u"{0} - {1}".format(self.queue, self.process)

    class Meta:
        app_label = 'process'
        verbose_name = _('Process Queue Item')
        verbose_name_plural = _('Process Queue Items')
        ordering = ('order',)


class Job(models.Model):
    image_source = models.ForeignKey(SourceImage)
    process_queue = models.ForeignKey(ProcessQueue)


class JobStep(models.Model):
    input_image = models.ImageField(null=True, blank=True)
    output_image = models.ImageField(null=True, blank=True)
    job = models.ForeignKey(Job)
    process = models.ForeignKey(ProcessQueueItem)

    models.ForeignKey(Job)
    models.ForeignKey(ProcessQueueItem)






