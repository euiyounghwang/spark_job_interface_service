#!/bin/bash
set -e

#tail -f ./logs/sparkjob-interface-api.log
sudo journalctl -u sparkjob_interface_api.service -f