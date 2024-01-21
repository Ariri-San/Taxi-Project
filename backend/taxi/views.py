from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models

# Create your views here.


class TravelViewSet(ModelViewSet):
    # serializer_class = serializers.TravelSerializer
    # permission_classes = [IsAuthenticated]
    
    
    # def get_permissions(self):
    #     return super().get_permissions()
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateTravelSerializer
        if self.request.method == "PUT":
            return serializers.UpdateUserTravelSerializer
        elif self.request.method == "GET":
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
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.History.objects.all()
        else:
            return models.History.objects.filter(user_id=user.id).all()

