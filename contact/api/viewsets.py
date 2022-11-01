from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactSerializer


class ContactAPI(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(**serializer.validated_data)
        return Response(serializer.data)