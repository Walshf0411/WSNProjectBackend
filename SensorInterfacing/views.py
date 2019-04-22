from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import Temprature_Record
from . import serializers
from rest_framework.response import Response
from .visualizations import do_visualization
from rest_framework import status
import numpy as np
from django.views.generic import TemplateView

# Create your views here.
class Receive_Data(CreateAPIView):  
    queryset = Temprature_Record.objects.all()
    serializer_class = serializers.Temprature_Data_Receiver_Serializer

class Get_visualization(APIView):
    
    def get(self, request, *args, **kwargs):
        # get the latest temprature of the 6 nodes.
        node1 = Temprature_Record.objects.filter(node="1").order_by("-date_received")[0].temprature
        node2 = Temprature_Record.objects.filter(node="2").order_by("-date_received")[0].temprature
        node3 = Temprature_Record.objects.filter(node="3").order_by("-date_received")[0].temprature
        node4 = Temprature_Record.objects.filter(node="4").order_by("-date_received")[0].temprature
        node5 = Temprature_Record.objects.filter(node="5").order_by("-date_received")[0].temprature
        node6 = Temprature_Record.objects.filter(node="6").order_by("-date_received")[0].temprature
        
        list_of_tempratures = [float(node1), float(node2), float(node3), float(node4), float(node5), float(node6)]
        # this is the path to the image that has been generated
        print("="*10 ,"Node temperatures", "="*10)
        print("Node 1": node1)
        print("Node 2": node2)
        print("Node 3": node3)
        print("Node 4": node4)
        print("Node 5": node5)
        print("Node 6": node6)
        path_to_image = do_visualization(
            np.array(list_of_tempratures)
        )
        return Response({
            'status': "Success",
            'path': path_to_image,
        }, status=status.HTTP_201_CREATED)

class View_Visualization(TemplateView):
    template_name = 'SensorInterfacing/get_visualization.html'

