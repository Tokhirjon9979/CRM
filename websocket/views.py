from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.models import Company
from company.permissions import IsNotificationOwner
from websocket import serializers
from websocket.models import Notifications


def randomNumberView(request):
    return render(request, 'index.html', context={'text': "hello world"})


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = serializers.NotificationsSerializer
    permission_classes = [IsAuthenticated, IsNotificationOwner]
    http_method_names = ('get', 'delete')

    def list(self, request, *args, **kwargs):
        queryset = Notifications.objects.filter(company__owner=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # user = request.user
        # print(user)
        # pk = kwargs.get("pk")
        # n = Notifications.objects.get(id=pk)
        # c = Company.objects.get(id=n.company_id)
        # if user == c.owner:
        #     n.is_seen = True
        # n.save()
        instance = self.get_object()
        instance.is_seen = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
