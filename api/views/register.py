from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.hashers import make_password
from api.serializers import model_serializer_factory
from core.models import User

class Register(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = model_serializer_factory(User, depth=0)
        serialized = serializer(data=request.data)

        if not serialized.is_valid():
            return Response({'status': 'unsuccessful', 'data': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serialized.save(password = make_password(serialized.validated_data['password']))
        
        #user = User.objects.get(mobile_number=serializer.validated_data['mobile_number'])
        #user.groups.add(settings.DEFAULT_GROUP)
        #user.save()

        return Response({'status': 'success', 'data': serializer(instance=serialized.instance, many=False).data}, status=status.HTTP_200_OK)
