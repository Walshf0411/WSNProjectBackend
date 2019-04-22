from rest_framework import serializers
from .models import Temprature_Record
import datetime
import csv

class Temprature_Data_Receiver_Serializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        validated_data['date_received'] = datetime.datetime.now()
        return super().create(validated_data)

    class Meta:
        model = Temprature_Record
        fields = ['node', 'temprature']