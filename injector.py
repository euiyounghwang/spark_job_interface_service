from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
from service.job_service import JobHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


# read host file to make an dict in memory
def read_hosts(server_file):
    server_list_dict = {}
    with open(server_file) as data_file:
        for line in data_file:
            if '#' in line:
                continue
            line = line.strip().split("|")
            # print(f"{line}")
            server_list_meta = []
            for meta in line:
                server_list_meta.append(meta)
            server_list_dict.update({line[0] : server_list_meta})
    return server_list_dict


hosts = read_hosts("./repository/hosts")
''' hosts = ['localhost', 'dev',...] '''
logger.info(list(hosts.keys()))
# es_hosts_enum_list =list(hosts.keys())


JobHandlerInject = JobHandler(logger, hosts)