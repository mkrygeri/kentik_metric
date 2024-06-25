# Kentik Metrics Module

This Python module provides functions for working with Kentik metrics.

## Dependencies

This module requires the following Python packages:

- yaml
- json
- requests
- logging
- os
- influx_line_protocol
- datetime
- influxdb_client

You can install these packages using pip:

```bash
pip install -r requirements.txt

import kentik_metrics


```markdown
# Kentik Metrics Module

This Python module provides functions for working with Kentik metrics.

## Dependencies

This module requires the following Python packages:

- yaml
- json
- requests
- logging
- os
- influx_line_protocol
- datetime
- influxdb_client

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

populate a config.yml with your API info apiEndpoint and deviceURI can be left alone unless you are sending to a cluster other than US.  
```yaml
kentik:
  apiEndpoint: 'https://grpc.api.kentik.com'
  deviceURI: '/device/v202308beta1/device'
  X-CH-Auth-Email: 'example@example.com'
  X-CH-Auth-API-Token: '09db8deadb33f12346745'
  debug: false
```

## Usage

First, import the module in your Python script:

```python
import kentik_metrics
```

If all goes well you will be able to send metrics into kentik. If a devices hasn't been created this will be handled automatically.


you will want to setup a few things in the dictionary. You will need to send the things you need for influx line protocol, but you will pass them as a dictionary. 
please see this link for more information https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/

here is an example of a record for a cpu metric for a server. Using an openconfig path for the metric is a good idea if it exists, but this is not required
records MUST contain the following a measurement name,  tags: 'device_name', 'ip_address' fields: at least one key/value pair
```dictionary format
metric_dict = {'/components/cpu/utilization', 'tags': {'device_name': 'server01', 'ip_address':'192.168.2.36','region': 'us-west'}, 'fields': {'mycpureading': 0.64}}
```

Once you have defined a dictionary, you may call the export function.
```
result = kentik_metric(metric_dict)
```
The function will send records by default. It will also return a string containing the influx formatted record that was sent. This may be useful if you would like to send this data to a local influxdb server. 
If you don't want to send the data to kentik but want to return the string, simply add send=False to the parameters.
```
result = kentik_metric(metric_dict,send=False)
```

## Contributing

If you want to contribute to this project, please submit a pull request.

## License

This project is licensed under the MIT License.
```

