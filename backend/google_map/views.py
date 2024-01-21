import googlemaps
import os
import environ
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .serializers import FindPlaceSerializer

# Create your views here.


env = environ.Env()
environ.Env.read_env()

key = os.environ['KEY']
gmaps = googlemaps.Client(key=key)


class FindPlace(APIView):
    def get(self, request, format=None):
        serializer = FindPlaceSerializer({"name":"ali"})
        return Response({"message": serializer.data})

    def post(self, request):
        serializer = FindPlaceSerializer(data=request.data)
        serializer.is_valid()
        
        name_search = serializer.data["name"]
        find_places = gmaps.find_place((name_search + ", UK"), "textquery")
        
        list_show = ["formatted_address", "name", "photos", "url", "geometry"]
        find_places_2 = []
        for i in find_places["candidates"]:
            place = gmaps.place(i["place_id"])["result"]
            find_places_2.append({j:place[j] for j in place if j in list_show})
        
        return Response({"places": find_places_2}, status=status.HTTP_200_OK)

