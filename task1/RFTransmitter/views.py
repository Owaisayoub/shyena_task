from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@api_view(['GET','POST'])
@csrf_exempt
def save_view(request):

    if request.method == 'GET':
        objs = UserProfile.objects.all()
        serializer = UserProfileSeralizer(objs, many = True)
        return Response(serializer.data)
    else:
        user_data = request.data
        log_table_data = user_data
        log_table_data["action"] = "save"
        serializer = UserProfileSeralizer(data = user_data)   
        if serializer.is_valid():
            serializer.save()
            serializer = LogTableSeralizer(data = log_table_data)
            if serializer.is_valid():
                serializer.save()            
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(serializer.errors)


@api_view(['GET','POST'])
@csrf_exempt
def start_stop_view(request):
    queryparameter = request.GET.get("action")
    status = "idle"
    if request.GET.get("action") == "start":
        status = "Active"
    
    log_table_data = request.data
    log_table_data["action"] = queryparameter
    serializers = LogTableSeralizer(data = log_table_data)
    if serializers.is_valid():
        serializers.save()
        res = serializers.data
        res["status"] = status
        return Response(res)
    return Response(serializers.errors)
    
