from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from villager_chess_api.models import TimeSetting
from villager_chess_api.serializers import TimeSettingSerializer, CreateTimeSettingSerializer

class TimeSettingView(ViewSet):
    """handles rest requests for time_setting objects"""
    def list(self, request):
        """handles GET requests for all time settings"""
        times = TimeSetting.objects.all()
        serialized = TimeSettingSerializer(times, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
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