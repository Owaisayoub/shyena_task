from RFTransmitter.views import *
from django.contrib import admin
from django.urls import path
from .views import save_view

urlpatterns = [
    path('save/', save_view),
    path('start-stop/', start_stop_view)

]