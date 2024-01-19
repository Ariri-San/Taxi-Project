from rest_framework import serializers
from . import models


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Travel
        fields = ['id', 'user', 'price', 'date', 'date_return', 'present', 'origin', 'destination', 'payment_status', 'travel_code']


class CreateTravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Travel
        fields = ['id', 'date', 'date_return', 'origin', 'destination']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.History
        fields = ['id', 'user', 'price', 'date', 'date_return', 'confirmed', 'origin', 'destination', 'travel_code']