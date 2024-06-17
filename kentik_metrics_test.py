from kentik_metrics import kentik_metric

# Use the function
metric_dict = {'metric':'/components/cpu/utilization','tags': {'device_name': 'server02','device_ip':'127.0.0.33', 'region': 'us-east'}, 'fields': {'mycpureading': 0.75}}
kentik_metric(metric_dict)


