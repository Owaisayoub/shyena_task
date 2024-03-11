from rest_framework import serializers
from .models import *


class UserProfileSeralizer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields =  '__all__'

        
class LogTableSeralizer(serializers.ModelSerializer):

    class Meta:
        model = LogTable
        fields =  '__all__'