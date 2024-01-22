from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models, api_google

# Create your views here.


class TravelViewSet(ModelViewSet):    
    def get_permissions(self):
        if self.request.method == 'DELETE': 
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if self.get_object().user == user or user.is_staff:
            return super().update(request, *args, **kwargs)
        return Response({"error": "You cant edit this Travel"})
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateTravelSerializer
        elif self.request.method == 'PUT':
            if self.request.user.is_staff:
                return serializers.UpdateAdminTravelSerializer
            else:
                return serializers.UpdateUserTravelSerializer
        else:
            return serializers.TravelSerializer
    

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.Travel.objects.all()
        else:
            return models.Travel.objects.filter(user_id=user.id).all()
    
    
    def get_serializer_context(self):
        user_id = self.request.user.id
        
        return {
            'user_id': user_id,
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }



class HistoryViewSet(mixins.ListModelMixin ,GenericViewSet):
    serializer_class = serializers.HistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.History.objects.all()
        else:
            return models.History.objects.filter(user_id=user.id).all()



class FindPlace(APIView):
    def get(self, request):
        serializer = serializers.FindPlaceSerializer({"name":"ali"})
        return Response({"message": serializer.data})

    def post(self, request):
        serializer = serializers.FindPlaceSerializer(data=request.data)
        serializer.is_valid()
        
        name_search = serializer.data["name"]
        try:
            find_places = api_google.ApiGoogle().find_places(name_search)
            return Response({"places": find_places}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Google Map Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FindDistance(APIView):
    def post(self, request):
        serializer = serializers.FindDistanceSerializer(data=request.data)
        serializer.is_valid()
        
        origin = serializer.data["origin"]
        destination = serializer.data["destination"]
        try:
            find_places = api_google.ApiGoogle().find_places(origin, destination)
            return Response({"places": find_places}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Google Map Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

