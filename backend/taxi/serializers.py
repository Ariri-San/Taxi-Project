import datetime
import pytz
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
    
    
    def check_times(self, validated_data):
        now = datetime.datetime.today().replace(tzinfo=pytz.UTC)
        
        if "date" not in validated_data:
            validated_data["date"] = now
        else:
            if validated_data["date"] < now:
                raise serializers.ValidationError({"date": ['Please Enter Currect Date.']})

        if "date_return" not in validated_data:
            date_return = False
        else:
            if validated_data["date_return"] <= validated_data["date"]:
                raise serializers.ValidationError({"date_return": ['Please Enter Currect Date Return.']})
            date_return = validated_data["date_return"]
        
        return date_return
    
    def create(self, validated_data):
        date_return = self.check_times(validated_data)
        
        google_map = api_google.ApiGoogle()
        
        origin_name, lat_origin, lng_origin = google_map.find_place(validated_data["origin"])
        origin, _ = models.Location.objects.get_or_create(name=origin_name, lat=lat_origin, lng=lng_origin)
        destination_name, lat_destination, lng_destination = google_map.find_place(validated_data["destination"])
        destination, _ = models.Location.objects.get_or_create(name=destination_name, lat=lat_destination, lng=lng_destination)
        
        distance = google_map.find_distance(
            origin=origin_name,
            destination=destination_name,
            date=validated_data["date"],
            date_return=date_return
            )
        
        if not distance:
            raise serializers.ValidationError('Api Google is not work!')
        
        validated_data["origin"] = origin
        validated_data["destination"] = destination
        return models.Travel.objects.create(**validated_data,
                                            price=distance["price"],
                                            user_id=self.context["user_id"],
                                            distance=distance["mile"],
                                            price_per_mile=distance["price_per_mile"])
    
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
    date = serializers.DateTimeField(label="Date")
    date_return = serializers.DateTimeField(label="Date Return")
    
    class Meta:
        fields = ["origin", "destination", "date", "date_return"]

    
class GetTravelSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="Id", required=True)
    
    class Meta:
        fields = ["id"]
