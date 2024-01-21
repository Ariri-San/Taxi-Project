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
    def get(self, request):
        serializer = FindPlaceSerializer({"name":"ali"})
        return Response({"message": serializer.data})

    def post(self, request):
        serializer = FindPlaceSerializer(data=request.data)
        serializer.is_valid()
        
        name_search = serializer.data["name"]
        try:
            find_places = gmaps.places_autocomplete(name_search, components={'country': ['UK']})
            
            list_show = ["formatted_address", "name", "url", "geometry"]
            find_places_2 = []
            for i in find_places:
                place = gmaps.place(i["place_id"])["result"]
                find_places_2.append({j:place[j] for j in place if j in list_show})
        except:
            return Response({"error": "Google Map Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"places": find_places_2}, status=status.HTTP_200_OK)

