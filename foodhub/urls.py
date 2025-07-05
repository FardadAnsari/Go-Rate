from django.urls import path
from .views import FoodHubView,YearlyBreakdownView,CachedStatsView


urlpatterns = [
    path('', FoodHubView.as_view(), name='some_view_name'),
    path('foodhub-yearly/', YearlyBreakdownView.as_view(), name='yearly_break_down'),
    path('foodhub-yearly-optimized/', CachedStatsView.as_view(), name='yearly_optimized_break_down'),

]