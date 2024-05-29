
import json
from service.status_handler import (StatusHanlder, StatusException)
import requests
from fastapi import Response
import pandas as pd



class JobHandler(object):
    
    def __init__(self, logger, hosts, sparkjob_list):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        ''' {'dev': ['dev', 'spkark jobs', 'localhost', '127.0.1']} '''
        self.logger = logger
        self.hosts = hosts
        self.sparkjob_list = sparkjob_list
        self.logger.info("__Init__ [hosts] : {}".format(self.hosts))
        self.logger.info("__Init__ [sparkjob_list]: {}".format(self.sparkjob_list))
                

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

            self.logger.info(f"get_active_spark_job : {spark_url}")
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

   
    async def get_all_active_sparkjobs(self):
        ''' get_all_active_sparkjobs in all evns from self.hosts'''
        try:

            self.logger.info(f"get_all_active_sparkjobs : {json.dumps(self.hosts)}")

            ''' get all env's spark jobs'''
            all_active_sparkjobs_dict = {}
            for v in self.hosts.values():
                ''' get hostname as master node in cluster for sparkjob'''
                master_node = v[2]
                ''' add a list of spark jobs on each node'''
                list_of_sparkjobs = await self.get_active_spark_job("http://{}:8080/json".format(master_node))
                
                each_rows = []
                if not isinstance(list_of_sparkjobs, (list)):
                    continue

                print(f"# list_of_sparkjobs - {list_of_sparkjobs}")
                all_active_sparkjobs_dict.update({master_node : list_of_sparkjobs})
            
                
            # self.get_active_spark_job
            self.logger.info(all_active_sparkjobs_dict)
           
            return all_active_sparkjobs_dict
            
        except Exception as e:
           return StatusException.raise_exception(str(e))
        

    async def get_download_excel_only_active_sparkjobs(self):
        '''
        Environment	Description	Server Name	IP Address	Job_Active_&_Online
            DEV	      test *    localhost   127.0.0.1	 testProcessEXP

        '''
        try:
            results = []
            for v in self.hosts.values():
                ''' get hostname as master node in cluster for sparkjob'''
                master_node = v[2]
                ''' add a list of spark jobs on each node'''
                list_of_sparkjobs = await self.get_active_spark_job("http://{}:8080/json".format(master_node))
                
                each_rows = []
                if not isinstance(list_of_sparkjobs, (list)):
                    # for element in v:
                    #     each_rows.extend([element])
                    # each_rows.append("no")
                    # results.append(each_rows)
                    continue

                # print(f"# list_of_sparkjobs - {list_of_sparkjobs}")
                list_of_spark_job_name = []
                for each_dict in list_of_sparkjobs:
                    for each_k, each_v in each_dict.items():
                        if each_k == 'name':
                            list_of_spark_job_name.append(each_v)

                
                ''' add basic metas'''
                for each_job_name in list_of_spark_job_name:
                    each_rows = []
                    for element in v:
                        each_rows.extend([element])
                    each_rows.append(each_job_name)
                    results.append(each_rows)
                
            # self.get_active_spark_job
            self.logger.info(results)
            
            df = pd.DataFrame(
                # [['Dev#1', "Dev spark job Dev spark job Dev spark job", "localhost", "localhost", "test_job"], ["Dev#2", "Dev spark job", "localhost", "localhost", "test_job"]], 
                results,
                columns=["Environment", "Description", "Server Name", "IP Address", "Job_Active_&_Online"]
            )

            return df
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        

    
    async def get_download_excel_all_sparkjobs(self):
        '''
        Environment	Description	Server Name	IP Address	Job_Active_&_Online
            DEV	      test *    localhost   127.0.0.1	 testProcessEXP

        '''
        try:
            results = []
            # sparkjob_name_list = ["StreamProcessEXP", "ArchiveProcess_OMx_EXP", "ArchiveElasticDelete_OMx_EXP", "ArchiveProcess_WMx_EXP", "ArchiveElasticDelete_WMx_EXP"]
            sparkjob_name_list = self.sparkjob_list
            for v in self.hosts.values():
                ''' get hostname as master node in cluster for sparkjob'''
                master_node = v[2]
                ''' add a list of spark jobs on each node'''
                list_of_sparkjobs = await self.get_active_spark_job("http://{}:8080/json".format(master_node))
                
                if not isinstance(list_of_sparkjobs, (list)):
                    for sparkjob_name in sparkjob_name_list:
                        each_rows = []
                        for element in v:
                            each_rows.extend([element])
                        each_rows.append(sparkjob_name)
                        each_rows.append("N")
                        # print("--#1 ", each_rows)
                        results.append(each_rows)
                        # print("--#2 ", results)
                    continue

                # print(f"# list_of_sparkjobs - {list_of_sparkjobs}")
                list_of_spark_job_name = []
                for each_dict in list_of_sparkjobs:
                    for each_k, each_v in each_dict.items():
                        if each_k == 'name':
                            list_of_spark_job_name.append(each_v)

                
                ''' add basic metas'''
                ''' looking for the active spark job which is in list_of_spark_job_name among all sparkjob_name_list'''
                for each_job_name in sparkjob_name_list:
                    each_rows = []
                    for element in v:
                        each_rows.extend([element])
                    if each_job_name in list_of_spark_job_name:
                        each_rows.append(each_job_name)
                        each_rows.append("Y")
                    else:
                        each_rows.append(each_job_name)
                        each_rows.append("N")
                    results.append(each_rows)
                
            # self.get_active_spark_job
            self.logger.info(results)
            
            df = pd.DataFrame(
                # [['Dev#1', "Dev spark job Dev spark job Dev spark job", "localhost", "localhost", "test_job", "Y"], ["Dev#2", "Dev spark job", "localhost", "localhost", "test_job", "N"]], 
                results,
                columns=["Environment", "Description", "Server Name", "IP Address", "Spark_Job_Name", "Job_Active_&_Online"]
            )

            return df
            # return {}
        
        except Exception as e:
           return StatusException.raise_exception(str(e))



    async def get_download_sparkjobs(self):
        ''' service layer '''
        ''' get_download_sparkjobs '''
        try:

            self.logger.info(f"get_download_sparkjobs : {json.dumps(self.hosts)}")

            ''' get all env's spark jobs'''
            ''' option1 : get_download_excel_only_active_sparkjobs '''
            # return await self.get_download_excel_only_active_sparkjobs()
        
            ''' get all env's spark jobs'''
            ''' option2 : get_download_excel_all_sparkjobs '''
            return await self.get_download_excel_all_sparkjobs()
            
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        
