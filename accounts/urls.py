from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'accounts'

urlpatterns = [
    path('add_employee/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('get_employee_data/<int:pk>/', views.AllEmployeeDataView.as_view(), name='get_employee_data'),
    path('delete_employee/', views.DeleteEmployeeView.as_view(), name='delete_employee'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
