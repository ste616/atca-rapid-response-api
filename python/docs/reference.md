# atca-rapid-response-api: Python library reference.

### Importing the library

We recommend importing the library as:

```python
import atca_rapid_response_api as arrApi
```

The rest of this documentation will assume this import directive.

### api class

The `api` class should be initialised with all required
properties, listed in a dictionary.

Assuming this dictionary is called `options`, you should
initialise the `api` class as:

```python
rapidRequest = arrApi.api(options)
```

#### options dictionary

The `options` dictionary has the following supported properties.
The properties are summarised in this table, and documented
fully later on this page.

| Property | Required? | Description |
| --- | --- | --- |
| `apiEndpoint` | No | The location of the web service on the web server |
| `authenticationToken` | Yes* | The token required to authenticate the request, as a string |
| `authenticationTokenFile` | Yes* | The name of the file that contains the token required to authenticate the request |
| `email` | Yes | The email address of the requester |
| `minimumTime` | No | The minimum amount of time required for this request to be useful, in hours |
| `nameCalibrator` | Yes | The name of a calibrator that is associated with the primary target |
| `nameTarget` | Yes | The name of the source that is the primary target of the request |
| `schedule` | Yes* | A string version of the CABB schedule |
| `scheduleFile` | Yes* | The name of the file to read in as a CABB schedule |
| `serverName` | No | The name of the webserver to use when sending the request to the web service |
| `serverProtocol` | No | The protocol to use when sending the request to the web service |


##### schedule

*This is a required property, although you may choose to
specify `scheduleFile` instead.*

