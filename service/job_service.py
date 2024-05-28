
import json
from service.status_handler import (StatusHanlder, StatusException)
import requests


class JobHandler(object):
    
    def __init__(self, logger):
        self.logger = logger
        
    
    async def get_download_sparkjobs(self):
        ''' query '''
        try:

            # result_json_value = database_object.excute_oracle_query(oas_query.get("sql"))
            # print(result_json_value, type(result_json_value))

            # return json.loads(str(result_json_value).replace("'",'"'))
            return {}
    
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        
