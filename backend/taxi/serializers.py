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
    
    
    def create(self, validated_data):
        if "date" not in validated_data:
            validated_data["date"] = datetime.datetime.today()
        
        google_map = api_google.ApiGoogle()
        
        origin_name, lat_origin, lng_origin = google_map.find_place(validated_data["origin"])
        origin, _ = models.Location.objects.get_or_create(name=origin_name, lat=lat_origin, lng=lng_origin)
        destination_name, lat_destination, lng_destination = google_map.find_place(validated_data["destination"])
        destination, _ = models.Location.objects.get_or_create(name=destination_name, lat=lat_destination, lng=lng_destination)
        
        distance = google_map.find_distance(
            origin=origin_name,
            destination=destination_name,
            date=validated_data["date"],
            date_return=validated_data["date_return"]
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
    
    class Meta:
        fields = ["origin", "destination"]

    
class GetTravelSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="Id", required=True)
    
    class Meta:
        fields = ["id"]
