from django.urls import path

from app1.views import HomeView, get_data, ChartData 

# app_name = 'app1'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/data/', get_data, name='api-data'),
    path('api/chart/data/', ChartData.as_view(), name='api-chart-data')
]
