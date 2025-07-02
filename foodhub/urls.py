from django.urls import path

from .views import FoodHubView


urlpatterns = [
    path('', FoodHubView.as_view(), name='some_view_name'),
]