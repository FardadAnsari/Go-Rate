from django.urls import path

from .views import JustEatView


urlpatterns = [
    path('', JustEatView.as_view(), name='some_view_name'),
]