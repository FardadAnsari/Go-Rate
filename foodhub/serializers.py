from rest_framework import serializers
from .models import FoodhubModel

class FoodHubSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", input_formats=["%Y-%m-%dT%H:%M:%S"])

    class Meta:
        model = FoodhubModel
        fields = '__all__'




