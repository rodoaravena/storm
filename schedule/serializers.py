from rest_framework import serializers
from schedule.models import ModuleTime, Schedule, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta:
        model = User    

class UserProfileSerializer(serializers.Serializer):
    rut = serializers.CharField(read_only=True)
    user = UserSerializer()
    class Meta:
        model = UserProfile

class ModuleTimeSerializer(serializers.Serializer):
    module = serializers.IntegerField(read_only=True)
    start = serializers.CharField(required=False, allow_blank=True, max_length=5)
    end = serializers.CharField(required=False, allow_blank=True, max_length=5)
    class Meta:
        model = ModuleTime

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField()
    created = serializers.DateTimeField()
    date_schedule = serializers.DateField()
    module = ModuleTimeSerializer()
    class Meta:
        model = Schedule
