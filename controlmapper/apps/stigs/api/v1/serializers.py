from rest_framework import serializers
import apps.stigs.models as benchmark_models
import re
from apps.rmf.api.v1.serializers import ControlCorrelationIdentifierSerializer


class CheckSerializer(serializers.ModelSerializer):
    check_content = serializers.SerializerMethodField()

    class Meta:
        model = benchmark_models.Check
        fields = ('id', 'check_content', 'system')

    def get_check_content(self, obj):
        if obj.check_content is None:
            rule_w_content = benchmark_models.Rule.objects.filter(version=obj.rule.version, checks__check_content__isnull=False).first()
            if rule_w_content is not None:
                check = rule_w_content.checks.filter(check_content__isnull=False).first()
                return check.check_content
        return obj.check_content


class FixSerializer(serializers.ModelSerializer):
    class Meta:
        model = benchmark_models.Fix
        fields = ('id', 'identifier', 'text')


class FixTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = benchmark_models.FixText
        fields = ('id', 'fixref', 'text')


class RuleSerializer(serializers.ModelSerializer):
    vuln_id = serializers.StringRelatedField(source='group.group_id', read_only=True)
    fix_text = serializers.SerializerMethodField()
    fix = serializers.SerializerMethodField()
    check = serializers.SerializerMethodField()
    ccis = ControlCorrelationIdentifierSerializer(many=True, read_only=True, required=False)
    description = serializers.SerializerMethodField()
    benchmark_name = serializers.SerializerMethodField()

    class Meta:
        model = benchmark_models.Rule
        fields = ('id', 'rule_id', 'title', 'vuln_id', 'fix_text',
                  'severity', 'ccis', 'benchmark_name',
                  'check', 'fix', 'version', 'description')

    @staticmethod
    def get_benchmark_name(obj):
        return obj.benchmark.get_friendly_name()

    @staticmethod
    def get_description(obj):
        try:
            description = re.match(r'<VulnDiscussion>([\S\s]*?)</VulnDiscussion>', obj.description).group(1)
        except AttributeError:
            description = obj.description
        return description

    @staticmethod
    def get_check(obj):
        if obj.checks.count() != 0:
            return obj.checks.first().check_content

    @staticmethod
    def get_fix_text(obj):
        if obj.fix_texts.count() != 0:
            return obj.fix_texts.first().text

    @staticmethod
    def get_fix(obj):
        if obj.fixes.count() != 0:
            return obj.fixes.first().text


class GroupSerializer(serializers.ModelSerializer):
    rules = RuleSerializer(many=True, read_only=True)

    class Meta:
        model = benchmark_models.Group
        fields = ('id', 'group_id', 'title', 'description', 'rules')


class ProfileSelectSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    ccis = serializers.SerializerMethodField()

    class Meta:
        model = benchmark_models.ProfileSelects
        fields = ('id', 'idref', 'selected', 'title', 'ccis')

    @staticmethod
    def get_ccis(obj):
        if obj.rule:
            return obj.rule.get_ccis()
        else:
            return obj.group.rules.first().get_ccis()

    @staticmethod
    def get_title(obj):
        if obj.rule:
            return obj.rule.title
        else:
            return obj.group.rules.first().title


class RuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = benchmark_models.Rule
        fields = ('id', 'rule_id', 'title')


class BenchmarkSerializer(serializers.ModelSerializer):
    identifier = serializers.SerializerMethodField()
    title = serializers.StringRelatedField(source='benchmark.title', read_only=True)
    release_info = serializers.SerializerMethodField()

    class Meta:
        model = benchmark_models.Benchmark
        fields = ('id', 'identifier', 'title', 'version', 'release_info', 'upload_completed')

    @staticmethod
    def get_identifier(obj):
        match = re.search(r'\_V(\d*?)R(\d*?)\_', obj.name)
        if match:
            return f"{obj.identifier.replace('_', ' ')} {match.group(0).strip('_')}"
        return f"{obj.identifier.replace('_', ' ')} V{obj.version}"


    @staticmethod
    def get_release_info(obj):
        try:
            return obj.plain_texts.filter(identifier='release-info').first().text
        except AttributeError:
            pass


class BenchmarkDetailSerializer(serializers.ModelSerializer):
    rules = serializers.SerializerMethodField()
    release_info = serializers.SerializerMethodField()
    identifier = serializers.SerializerMethodField()
    profiles = serializers.SerializerMethodField()
    class Meta:
        model = benchmark_models.Benchmark
        fields = ('id', 'identifier', 'title',
                  'status', 'upload_completed',
                  'rules', 'description', 'version', 'release_info', 'profiles')

    @staticmethod
    def get_release_info(obj):
        try:
            return obj.plain_texts.filter(identifier='release-info').first().text
        except AttributeError:
            pass

    @staticmethod
    def get_identifier(obj):
        return obj.get_friendly_name()

    @staticmethod
    def get_profiles(obj):
        return [{'identifier': profile.identifier, 'title': profile.title, 'selects': [select.idref for select in profile.selects.filter(selected=True)]} for profile in obj.profiles.all().prefetch_related('selects')]

    #
    # @staticmethod
    # def get_groups(obj):
    #     return GroupSerializer(obj.groups.filter(parent_group__isnull=True), many=True, read_only=True).data

    @staticmethod
    def get_rules(obj):
        return RuleSerializer(obj.rules.all().prefetch_related('ccis', 'fix_texts', 'checks', 'fixes'), many=True, read_only=True).data
