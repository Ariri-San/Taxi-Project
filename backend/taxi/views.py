from django.db import transaction
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


class HistoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin ,GenericViewSet):
    serializer_class = serializers.HistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.History.objects.all()
        else:
            return models.History.objects.filter(user_id=user.id).all()


class FixedPlacesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin ,GenericViewSet):
    queryset = models.FixedPrice.objects.all()
    serializer_class = serializers.FixedPriceSerializer
    permission_classes = [IsAuthenticated]



class TravelToHistory(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = serializers.GetTravelSerializer(data=request.data)
        serializer.is_valid()
        
        with transaction.atomic():
            travel_id = serializer.data["id"]
            travel = models.Travel.objects.get(id=travel_id) 

            history = models.History.objects.create(
                user = travel.user,
                price = travel.price,
                price_per_mile = travel.price_per_mile,
                distance = travel.distance,
                passengers = travel.passengers,
                luggage = travel.luggage,
                date = travel.date,
                date_return = travel.date_return,
                travel_code = travel.travel_code,
                origin = travel.origin,
                destination = travel.destination
            )
            
            history_serializer = serializers.HistorySerializer(data=history)
            history_serializer.is_valid()

            travel.delete()

            return Response({"comment": "history saved"}, status=status.HTTP_201_CREATED)


class FindPlace(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.FindPlaceSerializer(data=request.data)
        serializer.is_valid()
        
        find_places = api_google.ApiGoogle().find_places(serializer.data["name"])
        if find_places:
            return Response({"places": find_places}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Google Map Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FindDistance(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.FindDistanceSerializer(data=request.data)
        serializer.is_valid()

        find_distance = api_google.ApiGoogle().find_distance(origin=serializer.data["origin"], destination=serializer.data["destination"])
        if find_distance:
            return Response(find_distance, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Google Map Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CancelTravel(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.GetTravelSerializer(data=request.data)
        serializer.is_valid()
        
        travel_id = serializer.data["id"]
        travel = models.Travel.objects.get(id=travel_id)
        
        user = request.user
        if user.is_staff:
            travel.payment_status = "F"
        elif user == travel.user:
            if travel.payment_status == "P":
                travel.payment_status = "F"
            # if travel.payment_status == "C":
            #     travel.payment_status = "F"
            #     # api money
        travel.save()
        
        return Response({"comment": "travel Canceled"}, status=status.HTTP_200_OK)