from RFTransmitter.views import *
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('save/', SaveView.as_view()),
    path('start/', StartView.as_view()),
    path('stop/', StopView.as_view())

]