from rest_framework import serializers
from .models import JustEat


class JustEatSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%dT%H:%M:%S"])

    class Meta:
        model = JustEat
        fields = '__all__'