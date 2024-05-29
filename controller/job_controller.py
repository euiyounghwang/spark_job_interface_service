from fastapi import APIRouter
import json
import datetime
from injector import logger, JobHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import pandas as pd
from fastapi.responses import StreamingResponse
import datetime
from io import BytesIO
import xlsxwriter



''' Enter the host name of the master node in the spark cluster to collect the list of running spark jobs. '''
app = APIRouter(
    prefix="/spark",
)


'''
@app.get("/query", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/cluster/health?es_url=http://localhost:9200", 
          summary="DB Query")
async def get_db_query(es_url="http://localhost:9200"):
    # logger.info(es_url)
    # response =  SearchAPIHandlerInject.get_es_health(es_url)
    # if isinstance(response, dict):
    #     logger.info('SearchOmniHandler:get_es_info - {}'.format(json.dumps(response, indent=2)))

    return {}
'''


@app.get("/get_active_spark_job", 
          status_code=StatusHanlder.HTTP_STATUS_200,
        #   responses={
        #     200: {"description" : "OK"},
        #     404 :{"description" : "URl not found"}
        #   },
          description="Sample Payload : http://localhost:8003/spark/get_active_spark_job?spark_url=http://localhost:8080/json", 
          summary="Get the list of spark jobs in any env")
async def get_active_spark_job(spark_url="http://localhost:8080/json"):
    ''' get the information of spark jobs in the specific spark cluster '''
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
    response =  await JobHandlerInject.get_active_spark_job(spark_url)
    if isinstance(response, dict):
        logger.info('get_active_spark_job - {}'.format(json.dumps(response, indent=2)))

    return response



@app.get("/get_all_active_spark_job", 
          status_code=StatusHanlder.HTTP_STATUS_200,
        #   responses={
        #     200: {"description" : "OK"},
        #     404 :{"description" : "URl not found"}
        #   },
          description="Sample Payload : http://localhost:8003/spark/get_all_active_spark_job", 
          summary="Get the list of spark jobs in all env's")
async def get_all_active_spark_job():
    ''' get the information of spark jobs in all spark cluster '''
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
    response =  await JobHandlerInject.get_all_active_sparkjobs()
    if isinstance(response, dict):
        logger.info('get_all_active_sparkjobs - {}'.format(json.dumps(response, indent=2)))

    return response