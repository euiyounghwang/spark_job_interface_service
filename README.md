# spark_job_interface_service
<i>spark_job_interface_service

Apache Spark is an open-source unified analytics and data processing engine for big data. Its capabilities include near real-time or in-batch computations distributed across various clusters. 

Simply put, a Spark Job is a single computation action that gets instantiated to complete a Spark Action.  

- This repository searches the list of spark jobs running in the spark cluster currently in service.
- Additionally, they are created in Excel and downloaded.



### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry

# --
poetry config virtualenvs.in-project true
poetry init
poetry add fastapi
poetry add uvicorn
poetry add pytz
poetry add httpx
poetry add requests
poetry add xlsxwriter
poetry add openpyxl
```
or you can run this shell script `./create_virtual_env.sh` to make an environment. then go to virtual enviroment using `source .venv/bin/activate`



### Register Service
- sudo service sparkjob_interface_api status/stop/start/restart
```bash
#-- /etc/systemd/system/sparkjob_interface_api.service
[Unit]
Description=SparkJob Interface Service

[Service]
User=devuser
Group=devuser
Type=simple
ExecStart=/bin/bash /home/devuser/sparkjob_interface_api/service-start.sh
ExecStop= /usr/bin/killall sparkjob_interface_api

[Install]
WantedBy=default.target


# Service command
sudo systemctl daemon-reload 
sudo systemctl enable sparkjob_interface_api.service 
sudo systemctl start sparkjob_interface_api.service 
sudo systemctl status sparkjob_interface_api.service 
sudo systemctl stop sparkjob_interface_api.service 

sudo service sparkjob_interface_api status/stop/start
```



### Run Custom Promethues Exporter
- Run this command : $ `http://localhost:8003/docs`
