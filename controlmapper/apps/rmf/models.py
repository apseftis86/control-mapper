from django.db import models


class NistControl(models.Model):
    objects = models.Manager()

    control_type = models.CharField(max_length=20)
    baseline = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    # this may just be the statement.description
    number = models.CharField(max_length=20, db_index=True)
    family = models.CharField(max_length=255)
    title = models.CharField(max_length=250, null=True)
    revision = models.IntegerField()
    privacy_impact = models.CharField(max_length=5, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=(('P0', 'P0'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3')), null=True, blank=True)
    related = models.ManyToManyField('NistRelated', related_name='related_controls')
    parent_control = models.ForeignKey('self', related_name='enhancements', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.get_family()) + ': ' + str(self.get_number())

    def get_number(self):
        return self.number

    def get_family(self):
        return self.family

    def get_title(self):
        return self.title


class NistReference(models.Model):
    objects = models.Manager()

    href = models.TextField( null=True)
    text = models.TextField(null=True)
    short_name = models.TextField(null=True)
    control = models.ForeignKey(NistControl, related_name='references', on_delete=models.CASCADE)


class NistRelated(models.Model):
    objects = models.Manager()

    text = models.CharField(max_length=20)

class NistSupplementGuidanceRelatedItems(models.Model):
    objects = models.Manager()

    related = models.CharField(max_length=50)


class NistDiscussion(models.Model):
    objects = models.Manager()

    description = models.TextField()
    control = models.OneToOneField(NistControl, related_name='discussion', on_delete=models.CASCADE)


class NistSupplementalGuidance(models.Model):
    objects = models.Manager()

    description = models.TextField()
    control = models.OneToOneField(NistControl, related_name='supplemental_guidance', on_delete=models.CASCADE)
    related = models.ManyToManyField(NistSupplementGuidanceRelatedItems, related_name='related_items')


class NistStatement(models.Model):
    objects = models.Manager()

    number = models.CharField(max_length=25, null=True, db_index=True)
    description = models.TextField(null=True)
    statement = models \
        .ForeignKey('self', related_name='statements', null=True, on_delete=models.CASCADE)
    control = models \
        .OneToOneField(NistControl, related_name='statement', null=True, on_delete=models.CASCADE)
    parent_control = models \
        .ForeignKey(NistControl, related_name='nested_statements', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    def statement_control(self):
        if self.control:
            return self.control
        else:
            return self.parent_control

    def get_revision(self):
        if self.control:
            return self.control.revision
        else:
            return self.parent_control.revision


class ControlCorrelationIdentifier(models.Model):
    objects = models.Manager()

    name = models.TextField(null=True, unique=True)
    contributor = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    parameter = models.CharField(max_length=255, null=True, blank=True)
    publishdate = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    definition = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    statements = models.ManyToManyField(NistStatement, related_name='ccis')
    implementation_guidance = models.TextField(null=True, blank=True)
    assessment_procedures = models.TextField(null=True, blank=True)
    controls = models.ManyToManyField(NistControl, related_name='ccis', )

    def get_number(self):
        return int(str(self.name).replace('CCI-', ''))
