from fastapi import APIRouter
import json
import datetime
from injector import logger, JobHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional


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

@app.post("/download_excel_spark_job", description="download_excel_spark_job", summary="download_excel_spark_job")
async def get_download_sparkjobs():
    ''' Search to sparkjob in all envs '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        logger.info("get_download_sparkjobs")
        response_json = await JobHandlerInject.get_download_sparkjobs()
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        logger.info('Metrics : {}'.format(Delay_Time))

        # return {"running_time" : float(Delay_Time), "request_dbid" : db_id, "results" : response_json}
        return {}
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
    
        