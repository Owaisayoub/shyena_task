from rest_framework import serializers
from .models import *


class ConfigTableSeralizer(serializers.ModelSerializer):

    class Meta:
        model = ConfigTable
        fields =  '__all__'

        
class LogTableSeralizer(serializers.ModelSerializer):

    class Meta:
        model = LogTable
        fields =  '__all__'