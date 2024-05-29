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
          summary="Cluster Info")
async def get_active_spark_job(spark_url="http://localhost:8080/json"):
    ''' get spark jobs in the specific spark cluster '''
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


@app.get("/download_excel_spark_job", description="download_excel_spark_job", summary="download_excel_spark_job")
async def get_download_sparkjobs():
    ''' Search to sparkjob in all envs '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        logger.info("get_download_sparkjobs")
        df = await JobHandlerInject.get_download_sparkjobs()
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        logger.info('Metrics : {}'.format(Delay_Time))

        # return {"running_time" : float(Delay_Time), "request_dbid" : db_id, "results" : response_json}
        # return {}
        '''
        return df from service layer 
        df = pd.DataFrame(
                [["Canada", 10], ["USA", 20]], 
                columns=["team", "points"]
        )
        '''

        '''
        # -- csv
        return StreamingResponse(
                iter([df.to_csv(index=False)]),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=ES_SPARK_JOBS_{datetime.datetime.now().strftime('%Y%m%d')}.csv"}
                # headers={"Content-Disposition": f"attachment; filename=data.csv"}
        )
        '''
        # - getnerate excel file
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            header_format = workbook.add_format( # !!! here workable, no error
                {
                    'bold': True,
                    'text_wrap': True,
                    # 'valign': 'top',
                    'valign': 'center',
                    # 'fg_color': '#D7E4BC',
                    'bg_color': '#edbd93',
                    'border': 1
                }
            )

            column_settings = [{'header': column} for column in df.columns]
            (max_row, max_col) = df.shape

            # worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

            # Write the column headers with the defined format.
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.autofilter(0, 0, max_row, max_col - 1)
                worksheet.autofit()
                col_num += 1
            
        
        return StreamingResponse(
            BytesIO(buffer.getvalue()),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename=ES_SPARK_JOBS_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"}
        )
                
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
    

