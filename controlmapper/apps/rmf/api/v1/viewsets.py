from . import serializers as rmf_serializer
from apps.rmf import models as rmf_models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from lxml import etree
import json
from django.conf import settings
import logging

class ControlCorrelationIdentifierViewSet(viewsets.ModelViewSet):
    model = rmf_models.ControlCorrelationIdentifier
    queryset = model.objects.all().order_by('name')
    serializer_class = rmf_serializer.ControlCorrelationIdentifierSerializer
    serializer_detail_class = rmf_serializer.ControlCorrelationIdentifierSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name']

    @action(methods=['get'], detail=False)
    def update_ccis(self, request):
        # for cci in self.queryset:
        #     try:
        #         if cci.statement:
        #             cci.statements.add(cci.statement)
        #             cci.save()
        #     except:
        #         pass
        # file = open('/opt/mongo-app/ccis_rev3.json', 'r')
        # lines = file.readlines()
        # for line in lines:
        #     obj = json.loads(line)
        #     try:
        #         if obj['control']:
        #             statement = rmf_models.NistStatement.objects.filter( Q(Q(control__revision=3) | Q(parent_control__revision=3)), number=obj['control']['index']).first()
        #             if statement is not None:
        #                 cci_obj = rmf_models.ControlCorrelationIdentifier.objects.get(name=obj['@id'])
        #                 cci_obj.statements.add(statement)
        #                 cci_obj.save()
        #     except KeyError:
        #         pass
        # jsonObj = json.load(file)
        # for obj in jsonObj:
        #     print(obj)
        # with open('/opt/controls_export.csv/security.csv', "r") as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if row['CCI'] != 'CCI-0028888':
        #             cci = self.queryset.get(name=row['CCI'])
        #         cci.implementation_guidance = row['Implementation Guidance']
        #         cci.assessment_procedures = row['Assessment Procedures']
        #         cci.save()
        # ccis = self.model.objects.all()
        # for cci in ccis:
        #     statement = cci.statements.first()
        #     if statement is not None:
        #         cci.statement = statement
        #         cci.save()
        return Response({})


class NistStatementViewSet(viewsets.ReadOnlyModelViewSet):
    model = rmf_models.NistStatement
    queryset = model.objects.all()
    serializer_class = rmf_serializer.NistStatementSerializer
    serializer_detail_class = rmf_serializer.NistStatementSerializer


class CustomFilter(DjangoFilterBackend):
    model = rmf_models.NistControl
    queryset = model.objects.all()

    def filter_queryset(self, request, queryset, view):
        allowed_filters = ['statements__number',
                           'family',
                           'revision',
                           'number',
                           'impact_threshold',
                           'control_type']
        for key, value in request.query_params.items():
            if key not in allowed_filters:
                return queryset
            else:
                if key == 'statements__number':
                    queryset = queryset.filter(Q(statement__number=request.query_params.get('statements__number'))
                                               | Q(nested_statements__number=request.query_params.get('statements__number')))
                else:
                    queryset = queryset.filter(**{key:value})
        return queryset

#
# nsmap = {
#     'controls': "http://scap.nist.gov/schema/sp800-53/feed/2.0",
#     None: "http://scap.nist.gov/schema/sp800-53/2.0"
# }

nsmap = {
    'ns2': "http://www.w3.org/1999/xhtml",
    'ns3': "http://scap.nist.gov/schema/sp800-53/feed/1.0",
    None: "http://scap.nist.gov/schema/sp800-53/1.0"
}


def saveStatements(element, parent, parentType):
    if parentType == 'control':
        args = {'control': parent, 'number': parent.number}
    else:
        args = {'parent_control': parent.control if parent.control else parent.parent_control, 'statement': parent,  'number':  element.findtext('number', namespaces=nsmap)}
    args['description'] = element.findtext('description', namespaces=nsmap)
    ste_obj = rmf_models.NistStatement.objects.create(**args)
    # recursively save all other statements in statement
    for statement in element.findall('statement', namespaces=nsmap):
        saveStatements(statement, ste_obj, 'statement')


class NistControlViewSet(viewsets.ReadOnlyModelViewSet):
    model = rmf_models.NistControl
    queryset = model.objects.all().prefetch_related('statement__statements')
    serializer_class = rmf_serializer.NistControlListSerializer
    serializer_detail_class = rmf_serializer.NistControlSerializer
    filter_backends = [DjangoFilterBackend, CustomFilter]

    def get_serializer_class(self):
        if self.action == 'list':
            return super(NistControlViewSet, self).get_serializer_class()
        else:
            return self.serializer_detail_class or self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        for control in queryset.filter(control_type='enhancement', revision=5):
            try:
                discussion = rmf_models.NistDiscussion.objects.get(control=control)
                discussion.description = control.description
                discussion.save()
            except:
                pass
        context = {}
        if request.query_params.get('statements__number'):
            context = {'statement': request.query_params.get('statements__number')}
        serializer = self.serializer_class(queryset, many=True, context=context)
        return Response(serializer.data)

    # will show only the enhancements of a nist control
    @action(methods=['get'], detail=True)
    def enhancements(self, request, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info('Getting enhancements')
        instance = self.get_object()
        return Response(rmf_serializer.NistControlSerializer(instance.enhancements.all(), many=True).data)

    @action(methods=['get'], detail=False)
    def update_guidance(self, request):
        items = self.queryset
        for item in items:
            if item.description:
                supp_guidance = rmf_models.NistSupplementalGuidance.objects.create(description=item.description)
                item.supplemental_guidance = supp_guidance
                item.save()
        return Response({})

    def saveRev3Statements(self, element, parent, parentType):
        indexes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        if parentType == 'enhancement':
            print(parent.number)
        ste_obj, created = rmf_models.NistStatement.objects.get_or_create(description=self.getDescriptionText(element), number=parent.number, control=parent)
        statement_number = 0
        statements = self.getStatementObj(element)
        if statements is not None:
            for li in element.getchildren():
                if parentType == 'control':
                    args = {'parent_control': parent, 'number': parent.number + indexes[statement_number] + '.', 'statement': ste_obj}
                else:
                    args = {'parent_control': parent, 'number': parent.number + '(' + indexes[statement_number] + ')', 'statement': ste_obj}
                args['description'] = li.text
                rmf_models.NistStatement.objects.get_or_create(**args)
                statement_number += 1

    def getDescriptionObj(self, element):
        description = element.find('description', namespaces=nsmap)
        if description is not None:
            for child in description.getchildren():
                if etree.QName(child).localname == 'div':
                    return child

    def getDescriptionText(self, element):
        for child in element.getchildren():
            if etree.QName(child).localname == 'p':
                return child.text

    def getStatementObj(self, element):
        description = element.find('description', namespaces=nsmap)
        if description is not None:
            for child in description.getchildren():
                if etree.QName(child).localname == 'div':
                    for g_child in child.getchildren():
                        if etree.QName(g_child).localname == 'ol':
                            return g_child

    def getSupplementalGuidance(self, element):
        sg = element.find('supplemental-guidance', namespaces=nsmap)
        if sg is not None:
            for child in sg.getchildren():
                if etree.QName(child).localname == 'div':
                    for g_child in child.getchildren():
                        if etree.QName(g_child).localname == 'p':
                            return g_child.text


    @action(methods=['get'], detail=False, url_path='rev3')
    def nist_rev3(self, request):
        tree = etree.parse('/opt/mongo-app/nist_controlsrev3.xml')
        root = tree.getroot()
        for control in root.getchildren():
            control_obj, created = rmf_models.NistControl.objects.get_or_create(
                family=control.findtext('family', namespaces=nsmap),
                number=control.findtext('number', namespaces=nsmap).strip(),
                title=control.findtext('title', namespaces=nsmap),
                priority=control.findtext('priority', namespaces=nsmap),
                baseline=control.findtext('baseline-impact', namespaces=nsmap).strip() if control.findtext('baseline-impact', namespaces=nsmap) is not None else None,
                revision=3,
                control_type='control',
            )
            if self.getSupplementalGuidance(control) is not None:
                rmf_models.NistSupplementalGuidance.objects.get_or_create(control=control_obj, description=self.getSupplementalGuidance(control))
            # save statements on control starting with first statement
            description_obj = self.getDescriptionObj(control)
            if description_obj is not None:
                self.saveRev3Statements(description_obj, control_obj, 'control')
            # save all control enhancements
            control_enhancements = control.find('control-enhancements', namespaces=nsmap)
            if control_enhancements is not None:
                for enhancement in control_enhancements.findall('control-enhancement', namespaces=nsmap):
                    enh_obj, created = rmf_models.NistControl.objects.get_or_create(
                        number=control.findtext('number', namespaces=nsmap).strip() + '(' + enhancement.get('sequence') + ')',
                        baseline=enhancement.findtext('baseline-impact', namespaces=nsmap).strip() if enhancement.findtext('baseline-impact', namespaces=nsmap) is not None else None,
                        revision=3,
                        control_type='enhancement',
                    )
                    if self.getSupplementalGuidance(enhancement) is not None:
                        rmf_models.NistSupplementalGuidance.objects.get_or_create(control=enh_obj, description=self.getSupplementalGuidance(enhancement))
                    enh_obj.save()
                    description_obj = self.getDescriptionObj(enhancement)
                    if description_obj is not None:
                        self.saveRev3Statements(description_obj, enh_obj, 'enhancement')
                    # save related items inside of control enhancements
                    enh_obj.save()
            control_obj.save()
        return Response('Completed')

    @action(methods=['get'], detail=False, url_path='rev5')
    def nist_rev5(self, request):
        tree = etree.parse('/opt/mongo-app/nist_controls5.xml')
        root = tree.getroot()
        # for control in root.getchildren():
            # baseline = ''
            # for b in control.findall('baseline', namespaces=nsmap):
            #     baseline += b.text
            # # save anything text based
            # discussion = control.find('discussion', namespaces=nsmap)
            # control_obj = rmf_models.NistControl.objects.create(
            #     family=control.findtext('family', namespaces=nsmap),
            #     number=control.findtext('number', namespaces=nsmap),
            #     title=control.findtext('title', namespaces=nsmap),
            #     baseline=baseline if baseline != '' else None,
            #     description=discussion.findtext('description', namespaces=nsmap).strip() if discussion is not None else None,
            #     revision=5,
            #     control_type='control',
            # )
            # # get all related controls
            # for related in control.findall('related', namespaces=nsmap):
            #     related_obj, created = rmf_models.NistRelated.objects.get_or_create(text=related.text)
            #     control_obj.related.add(related_obj.id)
            # control_obj.save()
            # # save statements on control starting with first statement
            # statements = control.find('statement', namespaces=nsmap)
            # if statements is not None:
            #     saveStatements(statements, control_obj, 'control')
            # save all control enhancements
            # control_enhancements = control.find('control-enhancements', namespaces=nsmap)
            # if control_enhancements is not None:
            #     for enhancement in control_enhancements.findall('control-enhancement', namespaces=nsmap):
            #         discussion = enhancement.find('discussion', namespaces=nsmap)
            #         enh_obj = rmf_models.NistControl.objects.get(
            #             number=enhancement.findtext('number', namespaces=nsmap), revision=5
            #         )
            #         enh_obj.description = discussion.findtext('description', namespaces=nsmap).strip() if discussion is not None else None
            #         enh_obj.save()
                    # save statements inside of control-enhancements
                    # statements = enhancement.find('statement', namespaces=nsmap)
                    # if statements is not None:
                    #     saveStatements(statements, enh_obj, 'control')
                    # # save related items inside of control enhancements
                    # for related in enhancement.findall('related', namespaces=nsmap):
                    #     related_obj, created = rmf_models.NistRelated.objects.get_or_create(text=related.text)
                    #     enh_obj.related.add(related_obj.id)
                    # enh_obj.save()
            # references = control.find('references', namespaces=nsmap)
            # if references is not None:
            #     for reference in references.findall('reference',  namespaces=nsmap):
            #         item = reference.find('item',  namespaces=nsmap)
            #         if item is not None:
            #             rmf_models.NistReference.objects.create(
            #                 href=item.get('href'),
            #                 text=item.findtext('text',  namespaces=nsmap),
            #                 short_name=reference.findtext('text',  namespaces=nsmap),
            #                 control=control_obj
            #             )
            # control_obj.save()
        return Response('Complete')

    @action(methods=['get'], detail=False, url_path='thresholds')
    def get_thresholds(self, request):
        c_filter = self.model.objects.none()
        i_filter = self.model.objects.none()
        a_filter = self.model.objects.none()
        impact_filter = self.model.objects.none()
        thresholds = {}
        for key, value in request.query_params.items():
            if key in ['c', 'i', 'a', 'impact_threshold']:
                thresholds[key] = value
        for key, value in thresholds.items():
            if key == 'c':
                c_filter = self.model.objects.filter(Q(confidentiality_threshold__lte=thresholds['c']))
            if key == 'i':
                i_filter = self.model.objects.filter(Q(integrity_threshold__lte=thresholds['i']))
            if key == 'a':
                a_filter = self.model.objects.filter(Q(availability_threshold__lte=thresholds['a']))
            if key == 'impact_threshold':
                impact_filter = self.model.objects.filter(Q(impact_threshold__lte=int(thresholds['impact_threshold'])))
        queryset = c_filter | i_filter | a_filter | impact_filter
        return Response(self.serializer_class(queryset, many=True).data)
