from django.urls import path
from . import views

urlpatterns = [
    # takes in values, node number and temprature data
    path('send/', views.Receive_Data.as_view(), name='send_data'),
    path('get_visualization/', views.Get_visualization.as_view(), name='get_visualization'), 
    path('view_visualization/', views.View_Visualization.as_view(), name='view_visualization'),
]