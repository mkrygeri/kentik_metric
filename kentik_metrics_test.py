import time
import random
from kentik_metrics import kentik_metric,send_metrics

# 'serial-number':'','os-name':'','os-type':'','os-version','uptime-sec':'','boot-time':'','available':'','model':'','vendor':
while True:
    # Build a measurement
    metric_dict = {'measurement':'/components/cpu/utilization',
                    'tags': {'device_name': 'super-duper3',
                            'device_ip':'127.0.5.19', 
                            'region': 'us-east'}, 
                    'fields': {
                                'avg': random.randint(5, 100)},
                                'time': time.time_ns() }
    
    # Use the function
    result = kentik_metric(metric_dict)
    print(result)
    #send_metrics(result)
    metric_dict2 = {'measurement':'/system',
                   'tags': {'device_name': 'super-duper3',
                            'device_ip':'127.0.5.19',
                            'description': 'Solaris Server',
                            'model': 'Sun 4/260',
                            'region': 'us-east',
                            'os-name':'Solaris',
                            'os-type':'SYSV',
                            'os-version':'4.2'}, 
                    'fields':  {
                        'avg': random.randint(5, 100),
                        'online': True,
                        'available':1 ,
                        'uptime-sec':1, 
                        'boot-time':1},
                        'time': time.time_ns() }
    result2 = kentik_metric(metric_dict2)
    print(result2)
    #send_metrics(result2)   
    # Wait for 10 seconds
    time.sleep(.5)

