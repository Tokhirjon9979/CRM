from .views import randomNumberView
from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'notification', NotificationsViewSet)

urlpatterns = [
    path('', randomNumberView),
    path('', include(router.urls)),

]
