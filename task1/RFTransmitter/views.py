import subprocess
import os
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt



@method_decorator(csrf_exempt, name='dispatch')
class SaveView(APIView):
    
    def get(self, request):
        obj = ConfigTable.objects.last()
        serializers = ConfigTableSeralizer(obj)
        return serializers.data
    
    def post(self, request):
        config_data = request.data
        config_data["status"] = 'idle'
        last_row = ConfigTable.objects.last()
        if self.compare(config_data,ConfigTableSeralizer(last_row).data):
            return Response({
                'message': 'data Already present'
            })
        if last_row:
            process_id = last_row.pid
            last_row.pid = None
            last_row.status = "idle"
            last_row.save()
        data_for_log_table = request.data
        data_for_log_table["action"] = 'save'
        config_data_serilized = ConfigTableSeralizer(data  = config_data)
        if config_data_serilized.is_valid():
            config_data_serilized.save()
            log_table_serializer = LogTableSeralizer(data = data_for_log_table)
            if log_table_serializer.is_valid():
                log_table_serializer.save()
                response_obj = config_data_serilized.data
                del response_obj["pid"]
                return Response(response_obj)
            return Response(log_table_serializer.errors)
        return Response(config_data_serilized.errors)
            
    
    def compare(self, dict1, dict2):

        common_keys = set(dict1.keys()).intersection(dict2.keys())

        for key in common_keys:
            if dict1[key] != dict2[key]:
                return False
        return True
    
class StartView(APIView):

    def get(self, request):
        data = ConfigTable.objects.last()
        data_serialized = ConfigTableSeralizer(data_serialized)
        return Response(data_serialized.data)

    def post(self, request):
        data_in_db = ConfigTable.objects.all()
        if not  data_in_db:
            return Response({"message": "please save the configurations first"})
        user_data = request.data 
        user_table_last_row =ConfigTableSeralizer(ConfigTable.objects.last()).data
        log_table_last_row  = LogTableSeralizer(LogTable.objects.last()).data


        if not user_table_last_row:
            return 
        
        if log_table_last_row["action"] == "save" and self.compare(user_data, user_table_last_row):
            
            #Run the subprocess
            process_id = self.run_sub_process ()     

            #update the last row of the user table
            last_user = ConfigTable.objects.last()
            last_user.pid = process_id
            last_user.status = 'active'
            last_user.save()
            last_user_serialized = ConfigTableSeralizer(last_user)

            #store the log

            log_data = request.data
            log_data["action"] = 'start'
            log_data_serialized = LogTableSeralizer(data = log_data)
            if log_data_serialized.is_valid():
                log_data_serialized.save()
                return Response(last_user_serialized.data)
            return Response(log_data_serialized.errors)

        if log_table_last_row["action"] == "save" and not self.compare(user_data, user_table_last_row):
            res = self.save_start_different_data(request)
            return Response(res)


        if log_table_last_row["action"] == "start" and self.compare(user_data, user_table_last_row):
            return Response({
                "message": "system already running..."
            })
        # print("passed the same data with action start")

        if log_table_last_row["action"] == "start" and not self.compare(user_data, user_table_last_row):
            res = self.save_start_different_data(request)
            return Response(res)
        if log_table_last_row["action"] == 'stop' and self.compare(user_data,user_table_last_row):

            #Get the last row of config table
            config_last_row = ConfigTable.objects.last()


            #run the subprocess
            process_id = self.run_sub_process()

            #Change the status and store pid
            config_last_row.pid = process_id
            config_last_row.status = "start"
            config_last_row.save()
            config_last_row_serialized =ConfigTableSeralizer(config_last_row)

            #save the logs
            log_data = request.data 
            log_data["action"] = 'start'
            log_data_serialized = LogTableSeralizer(data= log_data)
            if log_data_serialized.is_valid():
                log_data_serialized.save()
                return Response(config_last_row_serialized.data)
            return Response({"message": "something went wrong"})

        if log_table_last_row["action"] == 'stop' and not self.compare(user_data,user_table_last_row):
            print('###############')
            #run new subprocess
            process_id = self.run_sub_process()
            #Store new configs
            config_data = request.data
            config_data["status"] = 'active'
            config_data["pid"] = process_id
            config_data_serialized = ConfigTableSeralizer(data=config_data)
            if config_data_serialized.is_valid():
                config_data_serialized.save()
            else:
                return Response(config_data_serialized.errors)
        
            #Take new Logs
            log_data = request.data
            log_data["action"] = 'start'
            log_data_serialized = LogTableSeralizer(data = log_data)
            if log_data_serialized.is_valid():
                log_data_serialized.save()
                return Response(config_data_serialized.data)
            return Response({"message": "something went wrong..."})
    
    
    def save_start_different_data(self,request):

        print('inside the save_start func')
        #Get the last row of config table
        config_table_last_row = ConfigTable.objects.last()
        if config_table_last_row.status == 'active': 
        
            #Get the process Id kill it  make it Null in DB and change  status to idle
            process_id = config_table_last_row.pid
            #kill here
            config_table_last_row.pid = None
            config_table_last_row.status = 'idle'
            config_table_last_row.save()

        #Run new subProcess
                
        process_id = self.run_sub_process()


        #save new configs in config table along with pid
        config_data = request.data
        config_data["pid"]= process_id
        config_data["status"]= "active"

        config_data_serialized = ConfigTableSeralizer(data =config_data)
        if config_data_serialized.is_valid():
            config_data_serialized.save()
        else:
            return config_data_serialized.errors

        #save new log in log table
        log_data = request.data
        log_data["action"] = 'start'

        log_data_serialized = LogTableSeralizer(data = log_data)
        if log_data_serialized.is_valid():
            log_data_serialized.save()
            print('save the log data')
            return config_data_serialized.data
        return log_data_serialized.errors     
        
    def run_sub_process(self):
        cmd = ["python3", "script.py"]  
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_id = process.pid
        return process_id
    
    def compare(self, dict1, dict2):
        common_keys = set(dict1.keys()).intersection(dict2.keys())
        for key in common_keys:
            if dict1[key] != dict2[key]:
                return False
        return True
    
        
class StopView(APIView):
    def get():
        pass
    def post(self,request):

        user_table_last_row = ConfigTable.objects.last()
        if not user_table_last_row:
            return Response({
                "message": "there is no process running"
            })
        if user_table_last_row.status == 'idle':
            return Response({
                "message": "System is already idle"
            })
        
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
        
