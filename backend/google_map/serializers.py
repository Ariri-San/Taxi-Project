from rest_framework import serializers


class FindPlaceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=511)

