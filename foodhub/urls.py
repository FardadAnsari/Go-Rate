from django.urls import path
from .views import FoodHubView,YearlyBreakdownView,FoodhubDailyCountView


urlpatterns = [
    path('', FoodHubView.as_view(), name='some_view_name'),
    path('foodhub-yearly/', YearlyBreakdownView.as_view(), name='yearly_break_down'),
    path('foodhub/', FoodhubDailyCountView.as_view(), name='yearly_break_down_1')
]