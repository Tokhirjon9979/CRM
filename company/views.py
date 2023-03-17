from rest_framework import viewsets, status
from rest_framework.response import Response

from websocket.models import Notifications
from .permissions import IsOwner, IsLocationOwner, IsLocationImagesOwner, IsCompanyOwnerorEmployee
from .serializers import CompanySerializer
from .models import Company, Product
from rest_framework.permissions import IsAuthenticated
from company import serializers

from accounts.models import User


# from django.contrib.auth.models import User


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def list(self, request, *args, **kwargs):
        queryset = Company.objects.filter(owner=request.user)  # queryset obyekt qaytarish uchun

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerorEmployee]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.filter(company__owner=request.user)  # queryset obyekt qaytarish uchun

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        company_id = request.data.get('company')
        company = Company.objects.get(id=company_id)
        if request.user != company.owner:
            return Response({'message': 'You are not owner of the company'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)

    def changes(self, old_data, new_data):
        s = " "
        for k in new_data:
            if old_data.get(k) != new_data[k]:
                s += f'{k}: {old_data.get(k)} changed to {new_data[k]}\n'
        return s

    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        pk = kwargs.get('pk')
        product = Product.objects.get(id=pk)
        # print(product.__dict__)
        # print(data)
        x = self.changes(product.__dict__, data)
        Notifications.objects.create(title=f'User:{user} tried to change {product}',
                                     description=f'User:{user}  {x}',
                                     company=product.company_id)

        return super().update(request, *args, **kwargs)
