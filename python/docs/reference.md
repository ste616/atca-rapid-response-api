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
| `emailOnly` | No | Send all emails only to this email address **(test mode only)** |
| `maximumLag` | No | The maximum time, in hours, that the service will schedule the start time from now |
| `minimumTime` | No | The minimum amount of time required for this request to be useful, in hours |
| `nameCalibrator` | Yes | The name of a calibrator that is associated with the primary target |
| `nameTarget` | Yes | The name of the source that is the primary target of the request |
| `noEmail` | No | Send no emails during the over-ride process **(test mode only)** |
| `noScoreLimit` | No | Assume that we can over-ride any observation **(test mode only)** |
| `noTimeLimit` | No | Assume that we can request an over-ride observation of any length **(test mode only)** |
| `schedule` | Yes* | A string version of the CABB schedule |
| `scheduleFile` | Yes* | The name of the file to read in as a CABB schedule |
| `serverName` | No | The name of the webserver to use when sending the request to the web service |
| `serverProtocol` | No | The protocol to use when sending the request to the web service |
| `test` | No | Set this to True to indicate that this is only a test request |
| `usePreviousFrequencies` | No | A Boolean indicator of whether the service should try and schedule using the frequencies that were being used at the start time |

##### apiEndpoint

*This is an optional property.* (**String**)

If you're submitting a request to the ATCA rapid response service, you probably don't
want to change this parameter from the default value `/cgi-bin/obstools/rapid_response/rapid_response_service.py`.

##### authenticationToken

*This is a required property, although you may choose to
specify `authenticationTokenFile` instead.* (**String**)

This parameter needs to be filled with a [JSON Web Token] (https://jwt.io) string that the ATCA rapid response
service will recognise as a valid authentication token. You will have been supplied an authentication token
by observatory staff, and this token must be passed back to the service.

Since the authentication token will have been supplied to you as a file, it is recommended that you pass the
token back by specifying the `authenticationTokenFile` parameter, rather than this parameter.

##### authenticationTokenFile

*This is a required property, although you may choose to
specify `authenticationToken` instead.* (**String**)

This parameter needs to be filled with the name of a readable file that contains a
[JSON Web Token] (https://jwt.io) string that the ATCA rapid response service will recognise as a valid
authentication token. You will have been supplied an authentication token file by observatory staff, and
if you pass the name of that file to this parameter, the library will read in the file, and automatically fill the
`authenticationToken` parameter with the string contained within.

##### email

*This is a required property.* (**String**)

You must specify an email address, which the over-ride service will use when sending notifications.
This email address must be one of those supplied on the OPAL proposal for your project. This
parameter is more of a security check than a necessary address.

##### emailOnly

*This is an optional property, and is only used for test requests* (**String**)

While you are testing your over-ride triggering software, you probably won't want to have emails sent to
your entire team and the teams of those projects you would have displaced. Specify an email address in
this parameter, and that will be the only address to receive any notifications from the over-ride
service.

##### maximumLag

*This is an optional property.* (**Float**)



##### schedule

*This is a required property, although you may choose to
specify `scheduleFile` instead.*

