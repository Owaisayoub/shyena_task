import subprocess
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
# @api_view(['GET','POST'])
# @csrf_exempt
# def save_view(request):

    # if request.method == 'GET':
    #     objs = UserProfile.objects.all()
    #     serializer = UserProfileSeralizer(objs, many = True)
    #     return Response(serializer.data)
    # else:
    #     user_data = request.data
    #     log_table_data = user_data
    #     log_table_data["action"] = "save"
    #     serializer = UserProfileSeralizer(data = user_data)   
    #     if serializer.is_valid():
    #         serializer.save()
    #         serializer = LogTableSeralizer(data = log_table_data)
    #         if serializer.is_valid():
    #             serializer.save()    
    #             res = serializer.data        
    #             return Response(serializer.data)
    #         return Response(serializer.errors)
    #     return Response(serializer.errors)

class SaveView(APIView):
    
    def get(self, request):
        obj = UserProfile.objects.last()
        serializers = UserProfileSeralizer(obj)
        return serializers.data
    
    def post(self, request):
        user_data = request.data
        user_data["status"] = 'idle'
        last_row = self.get(request)
        if self.compare(user_data,last_row):
            return Response({
                'message': 'data Already present'
            })
        data_for_log_table = request.data
        data_for_log_table["action"] = 'save'
        user_profile_serializer = UserProfileSeralizer(data  = user_data)
        if user_profile_serializer.is_valid():
            user_profile_serializer.save()
            log_table_serializer = LogTableSeralizer(data = data_for_log_table)
            if log_table_serializer.is_valid():
                log_table_serializer.save()
                response_obj = user_profile_serializer.data
                del response_obj["pid"]
                return Response(response_obj)
            return Response(log_table_serializer.errors)
        return Response(user_profile_serializer.errors)
            
    
    def compare(self, dict1, dict2):

        common_keys = set(dict1.keys()).intersection(dict2.keys())

        for key in common_keys:
            if dict1[key] != dict2[key]:
                return False
        return True
    
    



class StartView(APIView):
    def get():

        pass
    def post(self, request):

        command = ["python3", "script.py"]
        user_data = request.data
        user_data["action"] = "start"
        log_table_last_row = LogTable.objects.last()
        
        
        if self.compare(user_data, log_table_last_row):

            return Response({
                "message": "this aciton already in place"
            })
        
        if log_table_last_row.action != 'save':
            user_table_last_row = UserProfile.objects.last()
            if log_table_last_row.action == 'start':
                process_id = user_table_last_row.pid
                print("*****************")
                print(process_id)
                # os.kill(process_id, 15)
                user_table_last_row.pid = None
                user_table_last_row.status = 'idle'
                user_table_last_row.save()
            user_table_serializer = UserProfileSeralizer(data=user_data)
            if user_table_serializer.is_valid():
                user_table_serializer.save()
 

        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_pid = process.pid
        user_table_last_row = UserProfile.objects.last()
        user_table_last_row.status = 'active'
        user_table_last_row.pid = process_pid
        user_table_last_row.save()

        log_table_serializer = LogTableSeralizer(data = user_data)
        if log_table_serializer.is_valid():
            log_table_serializer.save()
            res = UserProfileSeralizer(user_table_last_row).data
            del res["pid"]
            return Response(res)
        return Response(log_table_serializer.errors)


    def query_log_table(self):
        obj = LogTable.objects.last()
        obj_serializer = LogTableSeralizer(obj)
        return obj_serializer.data
    def query_user_table(self):
        obj = UserProfile.objects.last()
        obj_serializer = UserProfileSeralizer(obj)
        return obj_serializer.data
    
    def compare(self, dict1, dict2):
        serialized_dict = UserProfileSeralizer(dict2).data

        common_keys = set(dict1.keys()).intersection(serialized_dict.keys())
        for key in common_keys:
            if dict1[key] != serialized_dict[key]:
                return False
        return True

# @api_view(['GET','POST'])
# @csrf_exempt
# def start_stop_view(request):
#     queryparameter = request.GET.get("action")
#     status = "idle"
#     if request.GET.get("action") == "start":
#         status = "Active"
    
#     log_table_data = request.data
#     log_table_data["action"] = queryparameter
#     # log_table_data["status"] = status

    
#     serializers = LogTableSeralizer(data = log_table_data)
#     if serializers.is_valid():
#         serializers.save()
#         res = serializers.data
#         res["status"] = status
#         return Response(res)
#     return Response(serializers.errors)
    
class StopView(APIView):
    def get():
        pass
    def post(self,request):

        user_table_last_row = UserProfile.objects.last()
        if not user_table_last_row:
            return Response({
                "message": "there is no process running"
            })
        if user_table_last_row.status == 'idle':
            return Response({
                "message": "System is already idle"
            })
        
        # log_table_last_row=LogTable.objects.last()
        # if log_table_last_row
        user_data = request.data
        user_data["action"]='stop'
        process_id=user_table_last_row.pid
        user_table_last_row.pid=None
        user_table_last_row.status='idle'
        user_table_last_row.save()
        #KILL KARNA HEIN
        log_table_serializer=LogTableSeralizer(data=user_data)
        if log_table_serializer.is_valid():
            log_table_serializer.save()
            res = log_table_serializer.data
            res["status"]=user_table_last_row.status
            return Response(res)
        return Response(log_table_serializer.errors)
        
