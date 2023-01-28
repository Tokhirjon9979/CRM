from rest_framework import viewsets
from .serializers import CompanySerializer
from .models import Company
from rest_framework.permissions import IsAuthenticated


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'patch', 'delete')
