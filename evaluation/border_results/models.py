from django.db import models

# Create your models here.


BORDER_CHOICES = (
    (0, 'None'),
    (10, 'Precise'),
    (20, 'Approximate'),
    (30, 'Not Useable'),
)


class Evaluation(models.Model):

    region_isolate = models.BooleanField(default=True)
    border_quality = models.IntegerField(choices=BORDER_CHOICES)


class ProcessResult(models.Model):

    name = models.CharField('Name', max_length=255)
    json_file = models.CharField('Json File', max_length=255, null=True, blank=True)
    category = models.CharField('Category', max_length=255)
    extra_data = models.TextField('Extra Data', null=True, blank=True)
    mask = models.CharField('Mask', max_length=511, null=True, blank=True)
    path = models.CharField('Path', max_length=511)

    source = models.CharField('Source', max_length=255)

    boundary_image = models.CharField('Boundary', max_length=511, null=True, blank=True)
    original_image = models.CharField('Cropped', max_length=511, null=True, blank=True)
    shape = models.CharField('Shape', max_length=127, blank=True, null=True)

    evaluation = models.ForeignKey(Evaluation, blank=True, null=True, related_name="results")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'source',)

    def setDataFromJson(self, data, file):
        self.json_file = file
        self.category = data['category']
        self.extra_data = data['extra_data']
        self.mask = data['mask']
        self.path = data['path']
        self.boundary_image = data['process_results']['boundary_image']
        self.original_image = data['process_results']['original_image']
        self.shape = ','.join([str(x) for x in data['process_results']['shape']])
        self.save()

        for item in data['process_results']['crop_to_center_log']:

            crop_to_center_log, created = CropToCenterLog.objects.get_or_create(process_result=self, segments=item['segments'])
            crop_to_center_log.forecount = ','.join([str(x) for x in item['forecount']])
            crop_to_center_log.shape = ','.join([str(x) for x in item['shape']])

            crop_to_center_log.save()

        for item in data['process_results']['size_index_threshold_log']:

            size_index_threshold_log, created = SizeIndexThresholdLog.objects.get_or_create(
                                                                                process_result=self,
                                                                                threshold=item['threshold'],
                                                                                touches_edges=False)
            if item['touches_edge']:
                size_index_threshold_log.touches_edges = True

            size_index_threshold_log.size_index = item['size_index']
            size_index_threshold_log.image_path = item['image_path']
            size_index_threshold_log.save()


class SizeIndexThresholdLog(models.Model):

    size_index = models.FloatField('Size Index', blank=True, null=True)
    threshold = models.FloatField('Threshold', blank=True, null=True)
    image_path = models.CharField('Image Path', max_length=511, null=True, blank=True)
    touches_edges = models.BooleanField('Touches Edges')

    process_result = models.ForeignKey(ProcessResult, related_name='+')

    class Meta:
        unique_together = ('process_result', 'threshold',)


class CropToCenterLog(models.Model):

    forecount = models.CharField('Foreground', max_length=127, null=True, blank=True)
    segments = models.IntegerField('Segments', null=True, blank=True)
    shape = models.CharField('Shape', max_length=10, null=True, blank=True)

    process_result = models.ForeignKey(ProcessResult, related_name='+')

    class Meta:
        unique_together = ('process_result', 'segments',)