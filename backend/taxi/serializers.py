from rest_framework import serializers
from . import models


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Travel
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage' ,'present', 'origin', 'destination', 'payment_status', 'travel_code']


class CreateTravelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        price = None
        return models.Travel.objects.create(**validated_data, price=price)
        
    
    class Meta:
        model = models.Travel
        fields = ['id', 'date', 'date_return', 'passengers','luggage','origin', 'destination']


class UpdateAdminTravelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Travel
        fields = ['payment_status', 'price', 'date', 'date_return', 'passengers','luggage','origin', 'destination']


class UpdateUserTravelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Travel
        fields = ['passengers', 'luggage', 'date', 'date_return']        


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.History
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage','confirmed', 'origin', 'destination', 'travel_code']