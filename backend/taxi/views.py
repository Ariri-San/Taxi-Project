from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models

# Create your views here.


class TravelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin ,GenericViewSet):
    queryset = models.Travel.objects.all()
    serializer_class = serializers.TravelSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateTravelSerializer
        elif self.request.method == "GET":
            return serializers.TravelSerializer


class HistoryViewSet(mixins.ListModelMixin ,GenericViewSet):
    queryset = models.History.objects.all()
    serializer_class = serializers.HistorySerializer
    # permission_classes = [IsAdminUser]

