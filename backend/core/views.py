from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import User
from .serializers import CheckAdminSerializer

# Create your views here.


class CheckAdmin(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CheckAdminSerializer(data=request.data)
        serializer.is_valid()

        try:
            if User.objects.filter(username=serializer.data["username"])[0].is_staff:
                return Response(True, status=status.HTTP_200_OK)
            else:
                return Response(False, status=status.HTTP_200_OK)
        except:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
            
