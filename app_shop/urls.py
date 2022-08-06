from django.urls import path
from .views import ShowOrders

urlpatterns = [
    path('main/', ShowOrders.as_view(), name="main"),
]