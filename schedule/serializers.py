from rest_framework import serializers
from schedule.models import Schedule, UserProfile
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

class ScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField()
    created = serializers.DateTimeField()
    date_schedule_start = serializers.DateTimeField()
    date_schedule_end = serializers.DateTimeField()
    class Meta:
        model = Schedule
