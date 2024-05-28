
import json
from service.status_handler import (StatusHanlder, StatusException)
import requests
from fastapi import Response
import pandas as pd



class JobHandler(object):
    
    def __init__(self, logger, hosts):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        ''' {'dev': ['dev', 'spkark jobs', 'localhost', '127.0.1']} '''
        self.logger = logger
        self.hosts = hosts
        self.logger.info("__Init__ : {}".format(self.hosts))
        

    async def get_active_spark_job(self, spark_url):
        ''' get_active_spark_job '''
        '''
        [
            {
                "starttime": 1716470965900,
                "id": "app-20240523092925-0002",
                "name": "TestProcessEXP",
                "cores": 10,
                "user": "test",
                "memoryperslave": 1024,
                "submitdate": "Thu May 23 09:29:25 EDT 2024",
                "state": "RUNNING",
                "duration": 455209407
            }
        ]
        '''
        try:

            self.logger.info(f"get_download_sparkjobs : {spark_url}")
             # -- make a call to master node to get the information of activeapps
            resp = requests.get(url=spark_url, timeout=5)
            
            if not (resp.status_code == 200):
                return None
            
            # logging.info(f"activeapps - {resp}, {resp.json()}")
            resp_working_job = resp.json().get("activeapps", "")
            # response_activeapps = []
            if resp_working_job:
                self.logger.info(f"activeapps - {resp_working_job}")
                return resp_working_job
            return None
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
   


    async def get_download_sparkjobs(self):
        ''' query '''
        try:

            # result_json_value = database_object.excute_oracle_query(oas_query.get("sql"))
            # print(result_json_value, type(result_json_value))

            # df = pd.DataFrame(
            #     [["Canada", 10], ["USA", 20]], 
            #     columns=["team", "points"]
            #  )
            
            # return StreamingResponse(
            #     iter([df.to_csv(index=False)]),
            #     media_type="text/",
            #     headers={"Content-Disposition": f"attachment; filename=./download/ES_SPARK_JOBS_20240514.xlsx"}
            # )

            df = pd.DataFrame(
                [["Dev#1", "Dev spark job", "localhost", "localhost", "test_job"], ["Dev#2", "Dev spark job", "localhost", "localhost", "test_job"]], 
                columns=["Environment", "Description", "Server Name", "IP Address", "Job_Active_&_Online"]
            )
            
            return df
            
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        
