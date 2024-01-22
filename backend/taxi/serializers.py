from datetime import datetime
from rest_framework import serializers
from . import models



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
        price_miles = models.PriceMile.objects.filter(is_active=True).all()
        price_mile = price_miles[0]
        
        joined_prices = models.JoinedPrice.objects.filter(pricemile=price_mile)
        
        joined_price = self.check_day(joined_prices)

        price = joined_price.priceday.price
        return models.Travel.objects.create(**validated_data, price=price, user_id=self.context["user_id"])
        
    
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