from datetime import datetime
from rest_framework import serializers
from . import models, api_google



class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Travel
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage' ,'present', 'origin', 'destination', 'payment_status', 'travel_code']


class CreateTravelSerializer(serializers.ModelSerializer):
    def check_day(self, joined_prices):
        now = datetime.now()
        day = now.isoweekday()
        if day == 7:
            day = "S"
        else:
            day = "O"
        time = now.time()
        
        for joined_price in joined_prices:
            start = joined_price.priceday.start
            finish = joined_price.priceday.finish
            if joined_price.day_of_week == day:
                
                if start < finish:
                    if start < time < finish:
                        return joined_price
                else:
                    if time > start or time < finish:
                        return joined_price
    
    
    def create(self, validated_data):
        try:
            price_miles = models.PriceMile.objects.filter(is_active=True).all()
            price_mile = price_miles[0]
            
            joined_prices = models.JoinedPrice.objects.filter(pricemile=price_mile)
            
            joined_price = self.check_day(joined_prices).priceday.price
            
            origin = validated_data["origin"]
            destination = validated_data["destination"]
            distance_meter = api_google.ApiGoogle().find_distance(origin=origin, destination=destination)
            if not distance_meter:
                raise serializers.ValidationError('Can Not Create Travel.')
            
            mile = float(distance_meter["distance_meter"]) * 0.000621371
            price = float(joined_price) * mile
            
            return models.Travel.objects.create(**validated_data,
                                                price=price,
                                                user_id=self.context["user_id"],
                                                distance=mile,
                                                price_per_mile=float(joined_price))
        except:
            raise serializers.ValidationError('Price dose not exist contact to support service.')
        
    
    class Meta:
        model = models.Travel
        fields = ['id', 'date', 'date_return', 'passengers', 'luggage', 'origin', 'destination']


class UpdateAdminTravelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Travel
        fields = ['payment_status', 'price', 'date', 'date_return', 'passengers', 'luggage', 'origin', 'destination']


class UpdateUserTravelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Travel
        fields = ['passengers', 'luggage', 'date', 'date_return']        


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.History
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage', 'confirmed', 'origin', 'destination', 'travel_code']

   
class FindPlaceSerializer(serializers.Serializer):
    name = serializers.CharField(label="Name", required=True, max_length=511)
    
    class Meta:
        fields = ["name"]


class FindDistanceSerializer(serializers.Serializer):
    origin = serializers.CharField(label="Origin", required=True, max_length=511)
    destination = serializers.CharField(label="Destination", required=True, max_length=511)
    
    class Meta:
        fields = ["origin", "destination"]

    
class TravelToHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(label="Id", required=True)
    
    class Meta:
        fields = ["id"]


class FixedPriceSerializer(serializers.Serializer):
    