import time
from kentik_metrics import kentik_metric

while True:
    # Build a measurement
    metric_dict = {'measurement':'/components/cpu/utilization','tags': {'device_name': 'server02','device_ip':'127.0.0.33', 'region': 'us-east'}, 'fields': {'avg': 75},'time': time.time_ns() }
    
    # Use the function
    result = kentik_metric(metric_dict)
    print(result)

    # Wait for 10 seconds
    time.sleep(10)

