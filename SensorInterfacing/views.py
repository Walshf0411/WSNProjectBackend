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
import requests
from WSN import settings

# Create your views here.
class Receive_Data(CreateAPIView):  
    queryset = Temprature_Record.objects.all()
    serializer_class = serializers.Temprature_Data_Receiver_Serializer

class Get_visualization(APIView):
    
    def get(self, request, *args, **kwargs):
        # get the latest temprature of the 6 nodes.
        # node1 = Temprature_Record.objects.filter(node="1").order_by("-date_received")[0].temprature
        # node2 = Temprature_Record.objects.filter(node="2").order_by("-date_received")[0].temprature
        # node3 = Temprature_Record.objects.filter(node="3").order_by("-date_received")[0].temprature
        # node4 = Temprature_Record.objects.filter(node="4").order_by("-date_received")[0].temprature
        # node5 = Temprature_Record.objects.filter(node="5").order_by("-date_received")[0].temprature
        #node6 = Temprature_Record.objects.filter(node="6").order_by("-date_received")[0].temprature

        # fetching data from thingspeak,     
        response = requests.get('https://api.thingspeak.com/channels/761799/feeds.json?api_key=DOAFDOS69FE9Y914&results=1')
        # get the json data received from the request.
        response_data = response.json()
        
        # getting the temperature from all the nodes.
        node_values = response_data['feeds'][0]
        nodes = []
        
        for i in range(1, settings.NUMBER_OF_NODES + 1):
            nodes.append(node_values['field' + str(i)])
        
        list_of_tempratures = [float(temperature) for temperature in nodes]

        print("="*10 ,"Node temperatures", "="*10)
        for i, node_temperature in enumerate(nodes):
            print("Node " + str(i) + ": " + str(node_temperature))

        path_to_image = do_visualization(
            np.array(list_of_tempratures), 
        )
        return Response({
            'status': "Success",
            'path': path_to_image,
        }, status=status.HTTP_201_CREATED)

class View_Visualization(TemplateView):
    template_name = 'SensorInterfacing/get_visualization.html'

