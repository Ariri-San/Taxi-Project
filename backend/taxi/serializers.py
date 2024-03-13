import datetime
from rest_framework import serializers
from . import models, api_google


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ["name", "lat", "lng"]


class TravelSerializer(serializers.ModelSerializer):
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    
    class Meta:
        model = models.Travel
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage' ,'present', 'origin', 'destination', 'payment_status', 'travel_code']


class CreateTravelSerializer(serializers.ModelSerializer):
    def validate_origin(self, origin):
        if not api_google.ApiGoogle().find_place(origin):
            raise serializers.ValidationError('Please Enter Currect Origin.')
        return origin
    
    def validate_destination(self, destination):
        if not api_google.ApiGoogle().find_place(destination):
            raise serializers.ValidationError('Please Enter Currect Destination.')
        return destination
    
    
    def check_day(self, joined_prices):
        now = datetime.datetime.now()
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
                    if start <= time <= finish:
                        return joined_price
                else:
                    if time > start or time < finish:
                        return joined_price
    
    
    def check_fixed_price(self, origin, destination):
        fixed_origin = models.FixedPrice.objects.filter(formated_address=origin).all()
        fixed_destination = models.FixedPrice.objects.filter(formated_address=destination).all()
        
        price = 0
        if fixed_origin:
            price = fixed_origin[0].price
        if fixed_destination:
            if fixed_destination[0].price > price:
                price = fixed_destination[0].price
        if price > 0:
            return price
        else:
            return False
    
    
    def create(self, validated_data):
        if "date" not in validated_data:
            validated_data["date"] = datetime.date.today()
        
        try:
            price_miles = models.PriceMile.objects.filter(is_active=True).all()
            price_mile = price_miles[0]
        except:
            raise serializers.ValidationError('Price Mile dose not exist contact to support service.')
        
        joined_prices = models.JoinedPrice.objects.filter(pricemile=price_mile)
        try:
            joined_price = self.check_day(joined_prices).priceday.price
        except:
            raise serializers.ValidationError('Price dose not exist contact to support service.')
        
        google_map = api_google.ApiGoogle()
        
        origin_name, lat_origin, lng_origin = google_map.find_place(validated_data["origin"])
        origin, _ = models.Location.objects.get_or_create(name=origin_name, lat=lat_origin, lng=lng_origin)
        destination_name, lat_destination, lng_destination = google_map.find_place(validated_data["destination"])
        destination, _ = models.Location.objects.get_or_create(name=destination_name, lat=lat_destination, lng=lng_destination)
        
        
        distance_meter = api_google.ApiGoogle().find_distance(origin=origin_name, destination=destination_name)
        if not distance_meter:
            raise serializers.ValidationError('Can Not Create Travel.')
        mile = float(distance_meter["distance_meter"]) * 0.000621371
        
        fixed_price = self.check_fixed_price(origin_name, destination_name)
        if fixed_price:
            price = fixed_price
        else:
            price = float(joined_price) * mile
        
        
        validated_data["origin"] = origin
        validated_data["destination"] = destination
        return models.Travel.objects.create(**validated_data,
                                            price=price,
                                            user_id=self.context["user_id"],
                                            distance=mile,
                                            price_per_mile=float(joined_price))
    
    origin = serializers.CharField(max_length=511)
    destination = serializers.CharField(max_length=511)
    
    class Meta:
        model = models.Travel
        fields = ['id', 'date', 'date_return', 'passengers', 'luggage', 'origin', 'destination']
        extra_kwargs = {
            "date": {"required": False},
        }


class UpdateAdminTravelSerializer(serializers.ModelSerializer):
    origin = LocationSerializer()
    destination = LocationSerializer()

    class Meta:
        model = models.Travel
        fields = ['payment_status', 'price', 'date', 'date_return', 'passengers', 'luggage', 'origin', 'destination']


class UpdateUserTravelSerializer(serializers.ModelSerializer):
    origin = LocationSerializer()
    destination = LocationSerializer()
      
    class Meta:
        model = models.Travel
        fields = ['passengers', 'luggage', 'date', 'date_return']        


class HistorySerializer(serializers.ModelSerializer):
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    
    class Meta:
        model = models.History
        fields = ['id', 'user', 'price', 'date', 'date_return', 'passengers', 'luggage', 'confirmed', 'origin', 'destination', 'travel_code']


class FixedPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FixedPrice
        fields = ["id", "name", "price", "formated_address"]

   
class FindPlaceSerializer(serializers.Serializer):
    name = serializers.CharField(label="Name", required=True, max_length=511)
    
    class Meta:
        fields = ["name"]


class FindDistanceSerializer(serializers.Serializer):
    origin = serializers.CharField(label="Origin", required=True, max_length=511)
    destination = serializers.CharField(label="Destination", required=True, max_length=511)
    
    class Meta:
        fields = ["origin", "destination"]

    
class GetTravelSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="Id", required=True)
    
    class Meta:
        fields = ["id"]
