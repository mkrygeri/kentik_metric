# kentik_metrics.py
#device_names = get_kentik_device_names()
import yaml
import json
import requests
import logging
import os
import time
from influx_line_protocol import Metric, MetricCollection
from datetime import datetime
import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS


#this function will load the config file
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"no config file found {config_file}: {e}")
        return None

kcfg = load_config('config.yml')
#This will load X-CH-Auth-API-Token from the environment or the config file
#print(kcfg)
#use the environment variables if they exist
if os.environ.get("X-CH-Auth-API-Token"):
    kentiktoken = os.environ['X-CH-Auth-API-Token']
else:
    kentiktoken = kcfg['kentik']['X-CH-Auth-API-Token']

if os.environ.get("X-CH-Auth-API-Email"):
    kentikemail = os.environ['X-CH-Auth-Email']
else:
    kentikemail = kcfg['kentik']['X-CH-Auth-Email']



headers ={}
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
client = influxdb_client.InfluxDBClient(
   url=metricsurl,
   token='',
   org='',
   debug=debug
)
write_api = client.write_api(write_options=SYNCHRONOUS)

#This will handle the sending of metrics to kentik and creating a device if needed
def kentik_metric(metric_dict,send=True):
    #print(metric_dict)
    #verify the required dict scructure is present
    if  'device_ip' not in metric_dict['tags'] or 'device_name' not in metric_dict['tags']:
        print('Cannot Send! required tags are device_name or device_ip are missing')
        return None
    if 'measurement' not in metric_dict:
        print('measurement key is missing')
        return None
    if 'tags' not in metric_dict:
        print('tags key is missing')
        return None
    if 'fields' not in metric_dict:
        print('fields key is missing')
        return None
    if 'time' not in metric_dict:   
        metric_dict['time'] = time.time_ns()
    #this will create a new device in kentik if it does not exist. Use wisely!
    if  metric_dict['tags']['device_name'] not in device_names:
            create_kentik_device(metric_dict['tags']['device_name'],metric_dict['tags']['device_ip'])
            device_names.append(metric_dict['tags']['device_name'])
    
    metric = influxdb_client.Point.from_dict(metric_dict)
    metric = str(metric)
    #metrics.append(metric)
    if send:
        send_metrics(metric)
    return metric

def send_metrics(metric):
    #for metric in metrics:
        try:
            response = requests.post(metricsurl, headers=headers, data=metric)
            if response.status_code == 204:
                print('metric sent')
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(e)
        #metric.clear()

#this funtion will give you a list of devices in kentik by device names only
def get_kentik_device_names():
    #print('getting kentik devices')
    response = requests.get(devicesurl, headers=headers)
    kentikDevices = json.loads(response.text)
    #print(kentikDevices)
    dev = [ sub['deviceName'] for sub in kentikDevices['devices'] ]
    #print(dev)
    return dev
device_names = get_kentik_device_names()

def gatherPlans():
    url = "https://api.kentik.com/api/v5/plans"
    payload = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            plan_data = json.loads(response.text)
            #print (plan_data)
        else:
            print(f"Error: {response.status_code}")
    except ConnectionError as exc:
         print(f"Connection error: {exc}")
    plan_dict = {}
    for plan in plan_data['plans']:
        #print(plan)
        if 'type' in plan['metadata']:
            plan_dict[plan['metadata']['type']] = {'id':plan['id'],'name':plan['name']}
        else:
            continue
        

    return plan_dict

#print(planid)

#this function will create a new device in kentik
def create_kentik_device(device_name,device_ip):
    plan_dict = gatherPlans()
    #print('creating kentik device')
    payload = json.dumps({
            "device": {
                "deviceName":  device_name,
                "deviceSnmpIp": device_ip,
                "site": "",
                "plan": {'id':plan_dict['metrics']['id'],'metadata': {'type':'metrics'}},
                "plan_id": plan_dict['flowpak']['id'],
                "labels": [],
                "deviceSnmpIp": device_ip,
                "minimize_snmp": True,
                "device_snmp_community": "",
                "device_type": "router",
                "device_subtype": "router",
                "device_flow_type": "auto",
                "device_sample_rate": "1",
                "sending_ips": [device_ip],
                "device_snmp_ip": device_ip,
                "device_sample_rate": 1,
                "device_bgp_type": "none"
            }
        })
    #print (payload)
    #print (headers)
    #print (devicesurl)
    try:
        kentikDevice = requests.request("POST", devicesurl, headers=headers, data=payload)
        if kentikDevice.status_code == 200:
            print(f"Device {device_name} created")
        else:
            print(f"Error: {kentikDevice.status_code}")
            print(f"Message: {kentikDevice.text}")
    except requests.exceptions.RequestException as e:
        print(e)
    print(kentikDevice.text)

if __name__ == "__main__":
    # Test the module
    metric_dict = {'metric': '/components/cpu/utilization','tags': {'device_name': 'server02', 'ip_address':'127.0.0.99' ,'region': 'us-east'}, 'fields': {'mycpureading': 0.75}}