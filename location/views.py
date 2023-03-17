from requests import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from accounts.models import User
from company.permissions import IsLocationOwner, IsLocationImagesOwner
from location import serializers
from location.models import Location, LocationImages


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [IsAuthenticated, IsLocationOwner]
    http_method_names = ('get', 'post', 'patch', 'delete')


class LocationImagesViewSet(viewsets.ModelViewSet):
    queryset = LocationImages.objects.all()
    serializer_class = serializers.LocationImagesSerializer
    permission_classes = [IsAuthenticated, IsLocationImagesOwner]
    parser_classes = (MultiPartParser,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        file = request.data['image']
        user = User.objects.get(username=username)
        user.image = file
        user.save()
        return Response({'message': 'Image  uploaded!'}, status=status.HTTP_200_OK)
