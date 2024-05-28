# spark_job_interface_service
<i>spark_job_interface_service

Apache Spark is an open-source unified analytics and data processing engine for big data. Its capabilities include near real-time or in-batch computations distributed across various clusters. 

Simply put, a Spark Job is a single computation action that gets instantiated to complete a Spark Action.  

- This repository searches the list of spark jobs running in the spark cluster currently in service.
- Additionally, they are created in Excel and downloaded.


#### Python V3.9 Install
```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz 
tar –zxvf Python-3.9.0.tgz or tar -xvf Python-3.9.0.tgz 
cd Python-3.9.0 
./configure --libdir=/usr/lib64 
sudo make 
Sudo make altinstall 

# python3 -m venv .venv --without-pip
sudo yum install python3-pip

sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

python3 -m venv .venv
source .venv/bin/activate

# pip install -r ./requirement.txt
pip install prometheus-client
pip install requests

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
```


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
sudo systemctl start sparkjob_interface_api.service 
sudo systemctl status sparkjob_interface_api.service 
sudo systemctl stop sparkjob_interface_api.service 

sudo service sparkjob_interface_api status/stop/start
```



### Run Custom Promethues Exporter
- Run this command : $ `http://localhost:8003/docs`
