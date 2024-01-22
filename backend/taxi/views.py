from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models, permissions

# Create your views here.


class TravelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delta = instance.present + timedelta(hours=12)
        
        if datetime.now().timestamp() <= delta.timestamp():
            return super().destroy(request, *args, **kwargs)
        return Response({
            "error": "You cant delete this Travel",
            "crated_time": f"{instance.present.date()}  {instance.present.time()}",
            "now_time": f"{datetime.now().date()}  {datetime.now().time()}",
        })
        
    
    
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
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.History.objects.all()
        else:
            return models.History.objects.filter(user_id=user.id).all()

