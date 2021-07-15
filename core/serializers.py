from rest_framework import serializers
from core.models import PastQuestion
class PastQuestionSerializer(serializers.ModelSerializer):
    semester = serializers.CharField(source="semester.__str__")
    course = serializers.CharField(source="course.__str__")
    class Meta:
        model = PastQuestion
        fields = ['semester', 'course', 'file', 'type']