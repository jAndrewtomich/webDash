from django.urls import path

from app2.views import HomeView, get_data, ChartData 


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('api/data/', get_data, name='api-data'),
    path('api/chart/data/', ChartData.as_view(), name='api-chart-data')
]