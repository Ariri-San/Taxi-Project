import datetime
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.conf import settings
from paypalrestsdk import notifications
from . import serializers, models, api_google

# Create your views here.


class TravelViewSet(ModelViewSet):    
    def get_permissions(self):
        if self.request.method == 'DELETE': 
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return models.Travel.objects.all()
        else:
            return models.Travel.objects.filter(user_id=user.id, payment_status="C").all()
    
    
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
    
    def get(self, request):
        travels = models.Travel.objects.all()
        serializer_travel = serializers.TravelSerializer(data=travels, many=True)
        serializer_travel.is_valid()
        
        return Response(data=serializer_travel.data, status=status.HTTP_200_OK)


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
        
        origin = serializer.data["origin"]
        destination = serializer.data["destination"]
        date = serializer.data["date"]
        date_return = serializer.data["date_return"]
        
        if not date:
            date = datetime.datetime.now()
        else:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
            except:
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            
        if date_return:
            try:
                date_return = datetime.datetime.strptime(date_return, '%Y-%m-%dT%H:%M')
            except:
                date_return = datetime.datetime.strptime(date_return, '%Y-%m-%dT%H:%M:%SZ')
            
        

        find_distance = api_google.ApiGoogle().find_distance(origin=origin, destination=destination, date=date, date_return=date_return)
        
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


class CompleteTravel(APIView):
    def post(self, request):
        if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
            return Response({"error":"TRANSMISSION_ID"}, status=status.HTTP_400_BAD_REQUEST)

        auth_algo = request.META['HTTP_PAYPAL_AUTH_ALGO']
        cert_url = request.META['HTTP_PAYPAL_CERT_URL']
        transmission_id = request.META['HTTP_PAYPAL_TRANSMISSION_ID']
        transmission_sig = request.META['HTTP_PAYPAL_TRANSMISSION_SIG']
        transmission_time = request.META['HTTP_PAYPAL_TRANSMISSION_TIME']
        webhook_id = settings.PAYPAL_WEBHOOK_ID
        event_body = request.body.decode(request.encoding or "utf-8")

        valid = notifications.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=transmission_time,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            actual_sig=transmission_sig,
            auth_algo=auth_algo,
        )

        if not valid:
            return Response({"error":"Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            travel = models.Travel.objects.get(id=transmission_id)
            travel.payment_status = "C"
            travel.save()
        except:
            return Response({"error":"Can Not Find Travel"}, status=status.HTTP_404_NOT_FOUND)
        
        # webhook_event = json.loads(event_body)

        # event_type = webhook_event["event_type"]

        # CHECKOUT_ORDER_APPROVED = "CHECKOUT.ORDER.APPROVED"

        # if event_type == CHECKOUT_ORDER_APPROVED:
        #     customer_email = webhook_event["resource"]["payer"]["email_address"]
        #     product_link = "https://learn.justdjango.com"
        #     send_mail(
        #         subject="Your access",
        #         message=f"Thank you for purchasing my product. Here is the link: {product_link}",
        #         from_email="your@email.com",
        #         recipient_list=[customer_email]
        #     )

            # Accessing purchased items when selling multiple products
            # webhook_event["resource"]["purchase_units"][0]["custom_id"]  # 'e-book-1234'
        
        return Response()

class PriceTravel(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.GetTravelSerializer(data=request.data)
        serializer.is_valid()
        
        travel_id = serializer.data["id"]
        
        # try:
        travel = models.Travel.objects.get(user=request.user, id=travel_id)
        return Response({"price": travel.price}, status=status.HTTP_200_OK)
        # except:
        #     return Response({"error":"Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
