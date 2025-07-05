from django.urls import path
from .views import FoodHubView,YearlyBreakdownView


urlpatterns = [
    path('', FoodHubView.as_view(), name='some_view_name'),
    path('foodhub-yearly/', YearlyBreakdownView.as_view(), name='yearly_break_down'),
]