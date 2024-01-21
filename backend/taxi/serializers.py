from rest_framework import serializers
from . import models


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Travel
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage' ,'present', 'origin', 'destination', 'payment_status', 'travel_code']


class CreateTravelSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
        
    
    class Meta:
        model = models.Travel
        fields = ['id', 'date', 'date_return', 'passengers','luggage','origin', 'destination']

class UpdateAdminTravelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Travel
        fields = ['payment_status', 'price', 'date', 'date_return', 'passengers','luggage','origin', 'destination']

class UpdateUserTravelSerializer(serializers.ModelSerializer):
    # def update(self, instance, validated_data):
    #     user_id = self.context['request'].user.id
    #     print(self.kwargs['pk'])    
    class Meta:
        model = models.Travel
        fields = ['passengers', 'luggage', 'date', 'date_return']        


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.History
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage','confirmed', 'origin', 'destination', 'travel_code']