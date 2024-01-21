import googlemaps
import os
import environ

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

env = environ.Env()
environ.Env.read_env()

key = os.environ['KEY']
gmaps = googlemaps.Client(key=key)

@api_view(['POST'])
def find_place(request):
    name_search = request.data["name"]
    
    find_places = gmaps.find_place((name_search + ", UK"), "textquery")
    
    return Response("sdf", status=status.HTTP_200_OK)