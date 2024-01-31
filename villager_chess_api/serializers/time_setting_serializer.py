from rest_framework import serializers
from villager_chess_api.models import TimeSetting

class TimeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSetting
        fields = ('id', 'time_amount', 'increment')

class CreateTimeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSetting
        fields = ['id', 'time_amount', 'increment']