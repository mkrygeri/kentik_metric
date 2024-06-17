# kentik_metrics.py
#device_names = get_kentik_device_names()
import yaml
import json
import requests
import yaml
import logging
import os
from influx_line_protocol import Metric, MetricCollection
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


headers ={}
#this function will load the config file
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config file {config_file}: {e}")
        return None

kcfg = load_config('config.yml')
#This will load X-CH-Auth-API-Token from the environment or the config file
print(kcfg)
if os.environ.get("kentiktoken"):
    kentiktoken = os.environ['X-CH-Auth-API-Token']
else:
    kentiktoken = kcfg['kentik']['X-CH-Auth-API-Token']

devicesurl = kcfg['kentik']['apiEndpoint'] + kcfg['kentik']['deviceURI']
metricsurl = kcfg['kentik']['apiEndpoint'] + kcfg['kentik']['metricURI']
headers['X-CH-Auth-API-Token'] = kentiktoken
headers['Content-Type'] = 'application/json'
headers['X-CH-Auth-Email'] = kcfg['kentik']['X-CH-Auth-Email']
debug = kcfg['kentik']['debug']
logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True
metrics=[]
#influxdb stuff
def kentik_metric(metric_dict):
    print(metric_dict)
    #this will create a new device in kentik if it does not exist. Use wisely!
    if  metric_dict['tags']['device_name'] not in device_names:
            create_kentik_device(metric_dict['tags']['device_name'],metric_dict['tags']['device_ip'])
            device_names.append(metric_dict['tags']['device_name'])
    metric = Metric(metric_dict['metric'])
    for key, value in metric_dict['tags'].items():
        metric.add_tag(key, value)
    for key, value in metric_dict['fields'].items():
        metric.add_value(key, value)
    metric.with_timestamp(0)
    metric = str(metric)
    #metrics.append(metric)
    try:
        response = requests.post(metricsurl, headers=headers, data=metric)
    except requests.exceptions.RequestException as e:
        print(e)
    print (metric)
    return metric

#this funtion will give you a list of devices in kentik by device names only
def get_kentik_device_names():
    #print('getting kentik devices')
    response = requests.get(devicesurl, headers=headers)
    kentikDevices = json.loads(response.text)
    dev = [ sub['deviceName'] for sub in kentikDevices['devices'] ]
    print(dev)
    return dev
device_names = get_kentik_device_names()

#this function will create a new device in kentik
def create_kentik_device(device_name,ip_address):
    #print('creating kentik device')
            payload = json.dumps({
            "device": {
                "deviceName":  device_name,
                "deviceSnmpIp": ip_address,
                "site": "",
                "plan_id": kcfg['kentik']['planid'],
                "labels": [],
                "deviceSnmpIp": ip_address,
                "minimize_snmp": True,
                "device_snamp_community": "kentikSNMP",
                "deviceType": "router",
                "plan": {
                    "id": kcfg['kentik']['planid'],
                    "name": "NMS Metrics"
                    },
                "sendingIps": [
                ip_address
                ],
                "device_sample_rate": "1",
                "device_subtype": "router",
                "device_bgp_type": "none"
            }
        })
            kentikDevice = requests.request("POST", devicesurl, headers=headers, data=payload)
            #print(kentikDevice.text)

if __name__ == "__main__":
    # Test the module
    metric_dict = {'metric': '/components/cpu/utilization','tags': {'device_name': 'server02', 'ip_address':'127.0.0.99' ,'region': 'us-east'}, 'fields': {'mycpureading': 0.75}}