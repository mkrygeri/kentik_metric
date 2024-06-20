import time
import random
from kentik_metrics import kentik_metric

while True:
    # Build a measurement
    metric_dict = {'measurement':'/components/cpu/utilization','tags': {'device_name': 'mikek-test','device_ip':'127.0.0.19', 'region': 'us-east'}, 'fields': {'avg': random.randint(5, 100)},'time': time.time_ns() }
    
    # Use the function
    result = kentik_metric(metric_dict)
    print(result)

    # Wait for 10 seconds
    time.sleep(10)

