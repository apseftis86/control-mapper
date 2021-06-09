from django.db import models
from lxml import etree
import re
from celery.utils.log import get_task_logger
from apps.rmf import models as rmf_models
logger = get_task_logger(__name__)


class CustomModelManager(models.Manager):

    def save_item(self, element, **kwargs):
        new_item = self.model()
        for k in kwargs:
            setattr(new_item, k, kwargs[k])
        new_item.save_item(element=element)
        new_item.save()
        return new_item

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(*args, **kwargs)


class CustomModel(models.Model):
    objects = CustomModelManager()

    class Meta:
        abstract = True
        ordering = ('id',)


class Benchmark(CustomModel):

    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    title = models.TextField()
    description = models.TextField()
    version = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        match = re.search(r'\_V(\d*?)R(\d*?)\_', str(self.name))
        if (match):
            return f"{self.identifier.replace('_', ' ')} {match.group(0).strip('_')}"
        return f"{self.identifier.replace('_', ' ')} V{self.version}"

    def get_friendly_name(self):
        match = re.search(r'\_V(\d*?)R(\d*?)\_', str(self.name))
        if (match):
            return f"{self.identifier.replace('_', ' ')}"
        return f"{self.identifier.replace('_', ' ')}"

    # friendly name with revision added
    def get_friendly_full_name(self):
        match = re.search(r'\_V(\d*?)R(\d*?)\_', str(self.name))
        if (match):
            return f"{self.identifier.replace('_', ' ')} {match.group(0).strip('_')}"
        return f"{self.identifier.replace('_', ' ')} V{self.version}"

    def save_item(self, element, **kwargs):
        text_attributes = ['title', 'description', 'version', 'status']
        # get identifier of benchmark for save
        self.identifier = element.get('id')
        self.save()
        profiles = []
        for child in element.getchildren():
            tag = etree.QName(child).localname
            # for title, description, version, status on benchmark
            if tag in text_attributes:
                # if there are nothing but text inside of <description>
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text if child.text is not None else ''
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                    setattr(self, tag, text)
                self.save()
            elif tag == 'plain-text':
                BenchmarkPlainText.objects.create(identifier=child.get('id'), text=child.text, benchmark=self)
            elif tag == 'Profile':
                # since profiles come in before rules and groups
                # we are going to put these in an array and hold on to them
                profiles.append(child)
            elif tag == 'Group':
                Group.objects.save_item(child, group_id=child.get('id'), benchmark=self)
            elif tag == 'Rule':
                Rule.objects.save_item(child, rule_id=child.get('id'), benchmark=self)
            elif tag == 'Value':
                Value.objects.save_item(child, identifier=child.get('id'), benchmark=self)
        for profile in profiles:
            Profile.objects.save_item(profile, identifier=profile.get('id'), benchmark=self)

    def update_item(self, element, **kwargs):
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if tag == 'Group':
                group = Group.objects.filter(benchmark=self, group_id=child.get('id')).first()
                if group is not None:
                    group.update_item(child)


class BenchmarkPlainText(CustomModel):
    

    identifier = models.CharField(max_length=100)
    text = models.TextField(null=True)
    benchmark = models.ForeignKey(Benchmark, related_name='plain_texts', on_delete=models.CASCADE)


# this is the profile from the STIG this will not be the profile that is mapped to the SSP benchmark for now.
class Profile(CustomModel):
    

    identifier = models.CharField(max_length=255)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    benchmark = models.ForeignKey(Benchmark, related_name='profiles', on_delete=models.CASCADE, null=True)

    def save_item(self, element, **kwargs):
        self.save()
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if tag == 'select':
                ProfileSelects.objects.save_item(child, idref=child.get('idref'), profile=self)
            else:
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                    setattr(self, tag, text)
                self.save()

    def update_item(self, element, **kwargs):
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if tag == 'select':
                select, created = ProfileSelects.objects.get_or_create(idref=child.get('idref'), profile=self)
                if created:
                    ProfileSelects.objects.save_item(child, profile=self)
            else:
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                    setattr(self, tag, text)
                self.save()


class ProfileSelects(CustomModel):
    

    idref = models.CharField(max_length=100)
    selected = models.BooleanField(default=True)
    profile = models.ForeignKey(Profile, related_name='selects', on_delete=models.CASCADE)
    # select will have either a group or a rule but not both
    group = models.ForeignKey('Group', related_name='selects', null=True, on_delete=models.CASCADE)
    rule = models.ForeignKey('Rule', related_name='selects', null=True, on_delete=models.CASCADE)

    def save_item(self, element, **kwargs):
        self.selected = element.get('selected').capitalize()
        # going to look for the group and the rule to the profile select to set foreign key
        try:
            group_obj = Group.objects.get(group_id=self.idref, benchmark=self.profile.benchmark)
            if group_obj is not None:
                self.group = group_obj
        except models.ObjectDoesNotExist:
            try:
                rule_obj = Rule.objects.get(rule_id=self.idref, benchmark=self.profile.benchmark)
                if rule_obj is not None:
                    self.rule = rule_obj
            except models.ObjectDoesNotExist:
                return
        self.save()


type_choices = [
    ('boolean', 'boolean'),
    ('number', 'number'),
    ('string', 'string')
]


class Value(CustomModel):
    

    identifier = models.CharField(max_length=255)
    title = models.TextField(blank=True)
    description = models.TextField(null=True, blank=True)
    operator = models.CharField(max_length=255)
    type = models.CharField(choices=type_choices, max_length=20)
    group = models.ForeignKey('Group', related_name='values', null=True, on_delete=models.CASCADE)
    benchmark = models.ForeignKey(Benchmark, related_name='values', on_delete=models.CASCADE)

    def save_item(self, element, **kwargs):
        self.save()
        for key in element.keys():
            # id is not usable in the model
            if key != 'id':
                if hasattr(self, key):
                    setattr(self, key, element.get(key))
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if tag == 'value':
                ValueValues.objects.create(value=self, value_text=child.text, selector=child.get('selector'))
            else:
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                    setattr(self, tag, text)
                self.save()


class ValueValues(CustomModel):
    

    selector = models.CharField(max_length=255, null=True)
    value_text = models.TextField()
    value = models.ForeignKey(Value, related_name='value_values', on_delete=models.CASCADE)


class Group(CustomModel):
    

    # when doing a check from the report item we will want to check the 'GROUP-ID' area first then
    # check if they have a 'Group-ID'
    group_id = models.CharField(max_length=255)
    title = models.TextField()
    version = models.CharField(max_length=100, null=True)
    description = models.TextField()
    benchmark = models.ForeignKey(Benchmark, related_name='groups', on_delete=models.CASCADE)
    parent_group = models.ForeignKey('self', related_name='groups', null=True, on_delete=models.CASCADE)

    def update_item(self, element):
        print(f"updating group {self.pk}")
        for child in element.getchildren():
            tag = etree.QName(child).localname
            print(tag)
            if tag == 'version':
                print(child.text)
                self.version = child.text
                self.save()

    def save_item(self, element, **kwargs):
        self.save()
        for child in element.getchildren():
            tag = etree.QName(child).localname
            text = None
            if hasattr(self, tag):
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                setattr(self, tag, text)
            self.save()
            if tag == 'Rule':
                Rule.objects.save_item(child, group=self, rule_id=child.get('id'), benchmark=self.benchmark)
            elif tag == 'Group':
                Group.objects.save_item(child, parent_group=self, group_id=child.get('id'), benchmark=self.benchmark)
            elif tag == 'Value':
                Value.objects.save_item(child, group=self, identifier=child.get('id'), benchmark=self.benchmark)


class Rule(CustomModel):
    

    rule_id = models.CharField(max_length=255, db_index=True)
    version = models.CharField(max_length=100, null=True)
    title = models.TextField()
    description = models.TextField()
    severity = models.CharField(max_length=10)
    group = models.ForeignKey(Group, related_name='rules', on_delete=models.CASCADE, null=True)
    benchmark = models.ForeignKey(Benchmark, related_name='rules', on_delete=models.CASCADE, null=True)
    # saving CCIs from the idents
    ccis = models.ManyToManyField(rmf_models.ControlCorrelationIdentifier, related_name='rules')

    def save_item(self, element, **kwargs):
        self.severity = element.get('severity')
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if hasattr(self, tag) and tag != 'check':
                if child.getchildren() is None:
                    setattr(self, tag, child.text)
                else:
                    text = child.text
                    # descriptions and other element can have <sub> or even <html> elements
                    # we are going to ignore those and only take in the text
                    for sub in child.getchildren():
                        text += sub.text
                        text += sub.tail
                    setattr(self, tag, text)
            else:
                self.save()
                if tag == 'ident':
                    if 'CCI' in child.text:
                        cci_obj, created = rmf_models.ControlCorrelationIdentifier.objects.get_or_create(name=child.text)
                        if cci_obj:
                            self.ccis.add(cci_obj)
                            self.save()
                elif tag == 'fix':
                    if child.text:
                        Fix.objects.save_item(child, rule=self)
                elif tag == 'fixtext':
                    FixText.objects.save_item(child, rule=self)
                elif tag == 'check':
                    Check.objects.save_item(child, rule=self)
            self.save()

    def get_ccis(self):
        return [cci.name for cci in self.ccis.all()]


class Check(CustomModel):
    

    system = models.CharField(max_length=255)
    check_content = models.TextField(null=True, blank=True)
    # normally these can be many but we will export these in a line separated manner
    rule = models.ForeignKey(Rule, related_name='checks', on_delete=models.CASCADE)

    def save_item(self, element, **kwargs):
        self.system = element.get('system')
        for child in element.getchildren():
            tag = etree.QName(child).localname
            if tag == 'check-content':
                self.check_content = child.text
        self.save()


class Fix(CustomModel):
    

    identifier = models.CharField(max_length=255)
    text = models.TextField()
    rule = models.ForeignKey(Rule, related_name='fixes', on_delete=models.CASCADE)

    def save_item(self, element, **kwargs):
        self.identifier = element.get('identifier')
        text = element.text
        # descriptions and other element can have <sub> or even <html> elements
        # we are going to ignore those and only take in the text
        for sub in element.getchildren():
            text += sub.text
            text += sub.tail
        self.text = text
        self.save()


class FixText(CustomModel):
    

    fixref = models.CharField(max_length=255)
    text = models.TextField()
    rule = models.ForeignKey(Rule, related_name='fix_texts', on_delete=models.CASCADE)

    def save_item(self, element, **kwargs):
        try:
            self.fixref = element.get('fixref')
        except:
            pass
        text = element.text
        # descriptions and other element can have <sub> or even <html> elements
        # we are going to ignore those and only take in the text
        for sub in element.getchildren():
            text += sub.text
            text += sub.tail
        self.text = text
        self.save()
