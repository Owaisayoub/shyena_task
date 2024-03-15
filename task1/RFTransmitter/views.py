import subprocess
import os
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt


class Generic:
    def update_config_table(self, current_status, process_id):
            last_user = ConfigTable.objects.last()
            last_user.pid = process_id
            last_user.status = current_status
            last_user.save()
            return last_user
    def store_log(self, action, log_data):
        log_data["action"] = action
        log_data = LogTableSeralizer(data = log_data)
        if log_data.is_valid():
            log_data.save()
            return True,log_data.data
        return False,log_data.errors 
    def store_new_configs(self, status, process_id, data):
        config_data = data
        config_data["status"] = status
        config_data["pid"] = process_id
        config_data = ConfigTableSeralizer(data=config_data)
        if config_data.is_valid():
            config_data.save()
            return True, config_data.data
        
        return False, config_data.errors
        

    
class SaveView(APIView,Generic):
    
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
            #kill the process id
            updated_last_row = self.update_config_table('idle', None)

        log_valid, log_res = self.store_log('save',request.data)
        config_valid, config_res = self.store_new_configs('idle', None, request.data)
        if not config_valid:
            return Response(config_res)
        if not log_valid:
            return Response(log_res)
        return Response(config_res)
            
    
    def compare(self, dict1, dict2):

        common_keys = set(dict1.keys()).intersection(dict2.keys())

        for key in common_keys:
            if dict1[key] != dict2[key]:
                return False
        return True
    
class StartView(APIView, Generic):

    def get(self, request):
        data = ConfigTable.objects.last()
        data = ConfigTableSeralizer(data)
        return Response(data.data)

    def post(self, request):
        data_in_db = ConfigTable.objects.all()
        if not  data_in_db:
            return Response({"message": "please save the configurations first"})
        user_data = request.data 
        user_table_last_row =ConfigTableSeralizer(ConfigTable.objects.last()).data
        log_table_last_row  = LogTableSeralizer(LogTable.objects.last()).data

        
        if log_table_last_row["action"] == "save" and self.compare(user_data, user_table_last_row): 
            #Run the subprocess
            process_id = self.run_sub_process ()     
            #update the last row of the user table
            last_user = ConfigTableSeralizer(self.update_config_table('start',process_id))
            #store the log
            save_success, res = self.store_log('start', request.data)
            if save_success:
                return Response(last_user.data)
            else:
                return Response(res)
            
        if log_table_last_row["action"] == "save" and not self.compare(user_data, user_table_last_row):
            res = self.save_start_different_data(request)
            return Response(res)


        if log_table_last_row["action"] == "start" and self.compare(user_data, user_table_last_row):
            return Response({
                "message": "system already running..."
            })

        if log_table_last_row["action"] == "start" and not self.compare(user_data, user_table_last_row):
            res = self.save_start_different_data(request)
            return Response(res)
        if log_table_last_row["action"] == 'stop' and self.compare(user_data,user_table_last_row):

            #Get the last row of config table
            config_last_row = ConfigTable.objects.last()


            #run the subprocess
            process_id = self.run_sub_process()

            #Change the status and store pid
            config_table_updated_last = self.update_config_table('active', process_id)
            config_last_row =ConfigTableSeralizer(config_table_updated_last)

            #save the logs
            valid, res = self.store_log('start', request.data)
            if not valid:
                return Response({"message": "something went wrong"})
            
            return Response(config_last_row.data)

        if log_table_last_row["action"] == 'stop' and not self.compare(user_data,user_table_last_row):
            #run new subprocess
            process_id = self.run_sub_process()
            #Store new configs
            valid ,config_res = self.store_new_configs('active',process_id,request.data)
            if not valid:
                print('not valid')
                return Response(res)
        
            #Take new Logs
            save_success, log_res = self.store_log('start', request.data)
            if save_success:
                return Response(config_res)
            return Response({"message": "something went wrong"})

    
    
    def save_start_different_data(self,request):
        print('inside the save_start func')
        #Get the last row of config table
        config_table_last_row = ConfigTable.objects.last()
        if config_table_last_row.status == 'active':  
            #Get the process Id kill it  make it Null in DB and change  status to idle
            process_id = config_table_last_row.pid
            #kill here
            last_user = self.update_config_table('idle', None)
        #Run new subProcess            
        process_id = self.run_sub_process()
        #save new configs in config table along with pid
        print('#############')
        valid, config_res = self.store_new_configs('active', process_id, request.data)
        print('@@@@@@@@', config_res)
        if not valid:
            
            return res
        #save new log in log table
        valid, res = self.store_log('start', request.data)
        return config_res
  
        
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
    
        
class StopView(APIView, Generic):
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
        process_id=user_table_last_row.pid
        updated_last_row = ConfigTableSeralizer(self.update_config_table('idle', None)).data
        
        #KILL KARNA HEIN
        data = ConfigTable.objects.last()
        # data = ConfigTableSeralizer(data).data
        data_for_log = {
            "type": data.type,
            "frequency": data.frequency,
            "prf": data.prf,
            "pw":data.pw
        }
        valid, log_res = self.store_log('stop',data_for_log)
        if not valid:
            return Response(log_res)
        return Response(updated_last_row)

        
