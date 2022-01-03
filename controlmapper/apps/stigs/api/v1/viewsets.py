from . import STIGViewSet
import apps.stigs.models as benchmark_models
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from . import serializers as stig_serializer
from apps.stigs import tasks
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


# currently application accepts xml and nessus files
def allowed_file(filename):
    acceptable_file_formats = ('nessus', 'xml')
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in acceptable_file_formats


class BenchmarkViewSet(STIGViewSet):
    model = benchmark_models.Benchmark
    queryset = model.objects.order_by('identifier')
    serializer_class = stig_serializer.BenchmarkSerializer
    serializer_detail_class = stig_serializer.BenchmarkDetailSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset().filter(id=pk).prefetch_related('groups__rules', 'rules').first()
        return Response(self.serializer_detail_class(queryset).data)

    @action(methods=['post'], detail=False)
    def upload_stig(self, request):
        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response('Error', status=400)
        if uploaded_file and allowed_file(uploaded_file.name):
            fs = FileSystemStorage()
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            fs.save(file_path, uploaded_file)
            existing_benchmark = benchmark_models.Benchmark.objects.filter(name=uploaded_file.name).first()
            if existing_benchmark is not None:
                # tasks.update_benchmark.delay(existing_benchmark.id, file_path)
                return Response('Benchmark already exists', status=409)
            else:
                benchmark = benchmark_models.Benchmark.objects.create(name=uploaded_file.name)
                if benchmark:
                    tasks.save_benchmark.delay(benchmark.id, file_path)
                    return Response('Benchmark successfully loaded', status=200)
                return Response('Something went wrong', status=400)
        return Response('Something went wrong', status=400)


# class ProfileViewSet(STIGViewSet):
#     model = benchmark_models.Profile
#     queryset = model.objects.all()
#     serializer_class = stig_serializer.Prof
#     serializer_detail_class = stig_serializer.ProfileSerializer
#     filter_fields = ['benchmark']
#
#     @action(methods=['get'], detail=True)
#     def snapshot_details(self, request, *args, **kwargs):
#         instance = self.get_object()
#         snapshot = request.query_params.get('snapshot')
#         if snapshot is None:
#             return Response('Must choose snapshot', status=400)
#         else:
#             if not instance.ssp.snapshots.filter(id=snapshot).exists():
#                 return Response('Profile not linked', status=400)
#             selects = instance.selects.filter(Q(group__rules__report_items__report_hosts__report__scan__snapshot=snapshot)).distinct()
#             return Response([{'idref': select.group.group_id if select.group else select.rule.rule_id,
#                               'status': select.get_report_item_status(snapshot)} for select in selects])
#

class ProfileSelectViewSet(STIGViewSet):
    model = benchmark_models.ProfileSelects
    queryset = model.objects.all()
    serializer_class = stig_serializer.ProfileSelectSerializer
    filter_fields = ['profile']

    @action(methods=['get'], detail=True, url_path='get-details')
    def get_details_from_id(self, request, *args, **kwargs):
        instance = self.get_object()
        rule = instance.rule if instance.rule else instance.group.rules.first()
        return Response([stig_serializer.RuleSerializer(rule).data])

    @action(methods=['get'], detail=False, url_path='get-details')
    def get_details_from_idref(self, request, *args, **kwargs):
        idref = request.query_params.get('idref')
        benchmark = request.query_params.get('benchmark')
        if idref and benchmark:
            group = benchmark_models.Group.objects.filter(group_id=idref, benchmark=benchmark)
            if group.exists():
                rule = group.rules.first()
            else:
                try:
                    rule = benchmark_models.Rule.objects.filter(rule_id=idref, benchmark=benchmark).first()
                except:
                    rule = None
            if rule:
                return Response([stig_serializer.RuleSerializer(rule).data])
            return Response('No rule found', status=404)
        else:
            return Response('Must get details based on idref and benchmark', status=400)



class GroupViewSet(STIGViewSet):
    model = benchmark_models.Group
    queryset = model.objects.all()
    serializer_class = stig_serializer.GroupSerializer


class RuleViewSet(STIGViewSet):
    model = benchmark_models.Rule
    queryset = model.objects.all()
    serializer_class = stig_serializer.RuleSerializer
    serializer_detail_class = stig_serializer.RuleSerializer
    filter_fields = {'rule_id': ['exact', 'in'],
                     'group__group_id': ['exact', 'in'],
                     'version': ['exact'],
                     'group__title': ['exact']}

    @action(methods=['get'], detail=False, url_path='item-map')
    def item_map(self, request, *args, **kwargs):
        rules = benchmark_models.Rule.objects.all()
        allowable_keys = ['rule_id', 'vuln_id', 'version', 'snapshot', 'ssp']
        for key, value in request.query_params.items():
            if key in allowable_keys:
                if key == 'rule_id':
                    rules = rules.filter(rule_id=value)
                if key == 'vuln_id':
                    rules = rules.filter(group__group_id=value)
                if key == 'version':
                    rules = rules.filter(version=value)
                if key == 'snapshot':
                    rules = rules.filter(benchmark__linked_ssps__ssp__snapshots=value)
                if key == 'ssp':
                    rules = rules.filter(benchmark__linked_ssps__ssp=value)
        serializer = self.serializer_detail_class(rules, many=True)
        return Response(serializer.data)
