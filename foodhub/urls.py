from django.urls import path
from .views import FoodHubView,YearlyBreakdownView,Foodhub10DayStatsView


urlpatterns = [
    path('', FoodHubView.as_view(), name='some_view_name'),
    path('foodhub-yearly/', YearlyBreakdownView.as_view(), name='yearly_break_down'),
    path('foodhub/', Foodhub10DayStatsView.as_view(), name='yearly_break_down_1')
]