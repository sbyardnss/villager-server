from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import TimeSetting

class TimeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSetting
        fields = ('id', 'time_amount', 'increment')

class CreateTimeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSetting
        fields = ['id', 'time_amount', 'increment']

class TimeSettingView(ViewSet):
    """handles rest requests for time_settings"""
    def list(self, request):
        """handles GET requests for all time settings"""
        times = TimeSetting.objects.all()
        serialized = TimeSettingSerializer(times, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def list(self, request, pk=None):
        """handles GET requests for single time settings"""
        time = TimeSetting.objects.get(pk=pk)
        serialized = TimeSettingSerializer(time, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        """handles POST requests to time settings"""
        serialized = CreateTimeSettingSerializer(data = request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)