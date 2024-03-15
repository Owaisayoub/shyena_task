from django.contrib import admin
from RFTransmitter.models import ConfigTable, LogTable

# Register your models here.

# admin.site.register([UserProfile, LogTable]


admin.site.register([ConfigTable, LogTable])
