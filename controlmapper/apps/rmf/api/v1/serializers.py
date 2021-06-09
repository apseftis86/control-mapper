from rest_framework import serializers
import apps.rmf.models as rmf_models
from django.db.models import Q


# for CCIS
class ControlCorrelationIdentifierSerializer(serializers.ModelSerializer):
    controls = serializers.SerializerMethodField(required=False)

    class Meta:
        model = rmf_models.ControlCorrelationIdentifier
        fields = ('name', 'controls', 'definition', 'type', 'parameter', 'implementation_guidance', 'assessment_procedures')

    @staticmethod
    def get_controls(obj):
        controls = []
        for statement in obj.statements.all():
            revision = statement.get_revision()
            controls.append({'number': statement.number,
             'revision': revision})
            if revision == 4:
                controls.append({'number': statement.number,
                                 'revision': 5})
        return controls


class NistStatementSerializer(serializers.ModelSerializer):
    statements = serializers.SerializerMethodField(required=False)
    ccis = serializers.SerializerMethodField(required=False)

    class Meta:
        model = rmf_models.NistStatement
        fields = ('number', 'description', 'statements', 'ccis')

    @staticmethod
    def get_statements(obj):
        return NistStatementSerializer(obj.statements.all(), many=True, required=False, read_only=True).data

    @staticmethod
    def get_ccis(obj):
        if obj.get_revision() in [3, 4]:
            return [cci.name for cci in obj.ccis.all()]
        else:
            ccis = rmf_models.ControlCorrelationIdentifier.objects.filter(Q(Q(statements__control__revision=4) | Q(statements__parent_control__revision=4)), statements__number=obj.number)
            return [cci.name for cci in ccis]


class NistControlListSerializer(serializers.ModelSerializer):
    requested_statement = serializers.SerializerMethodField(required=False)
    statement = NistStatementSerializer(required=False, read_only=True)
    description = serializers.SerializerMethodField(required=False)

    class Meta:
        model = rmf_models.NistControl
        fields = ('id','family', 'number', 'title', 'description', 'statement',
                  # 'confidentiality_threshold', 'integrity_threshold',  'availability_threshold',
                  # 'impact_threshold',
                  'requested_statement',
                  # 'supplemental_guidance'
                  )

    @staticmethod
    def get_nested_statements(obj):
        if obj.revision == 3:
            return NistStatementSerializer(obj.nested_statements.all(), many=True).data

    @staticmethod
    def get_description(obj):
        attr = 'supplemental_guidance' if obj.revision != 5 else 'discussion'
        try:
            attr_obj = getattr(obj, attr)
            return attr_obj.description
        except AttributeError:
            return None

    @staticmethod
    def get_control(obj):
        if obj.revision in [3, 5]:
            return obj.statement.description
        elif obj.revision == 4:
            return obj.control

    def get_requested_statement(self, obj):
        try:
            statement = self.context['statement']
            if statement != obj.number:
                return statement
        except KeyError:
            pass


class NistControlSerializer(serializers.ModelSerializer):
    statement = NistStatementSerializer(required=False, read_only=True)
    description = serializers.SerializerMethodField(required=False)
    control = serializers.SerializerMethodField(required=False)

    class Meta:
        model = rmf_models.NistControl
        fields = ('id', 'family', 'number', 'title', 'control', 'description', 'statement',
                  # 'confidentiality_threshold',  'integrity_threshold',  'availability_threshold',
                  )

    @staticmethod
    def get_description(obj):
        attr = 'supplemental_guidance' if obj.revision == 4 else 'discussion'
        try:
            attr_obj = getattr(obj, attr)
            return attr_obj.description
        except AttributeError:
            return None

    @staticmethod
    def get_control(obj):
        if obj.revision == 5:
            return obj.statement.description
        else:
            return obj.control




