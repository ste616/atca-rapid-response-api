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

| Property | Required? | Type | Description |
| --- | --- | --- | --- |
| `apiEndpoint` | No | String | The location of the web service on the web server |
| `authenticationToken` | Yes* | String | The token required to authenticate the request, as a string |
| `authenticationTokenFile` | Yes* | String | The name of the file that contains the token required to authenticate the request |
| `email` | Yes | String | The email address of the requester |
| `emailOnly` | No | String | Send all emails only to this email address **(test mode only)** |
| `maximumLag` | No | Float | The maximum time, in hours, that the service will schedule the start time from now |
| `maxTime` | No | Float | The maximum amount of time to allocate to this request, in hours **(test mode only)** |
| `minimumTime` | No | Float | The minimum amount of time required for this request to be useful, in hours |
| `nameCalibrator` | Yes | String | The name of a calibrator that is associated with the primary target |
| `nameTarget` | Yes | String | The name of the source that is the primary target of the request |
| `noEmail` | No | Boolean | Send no emails during the over-ride process **(test mode only)** |
| `noScoreLimit` | No | Boolean | Assume that we can over-ride any observation **(test mode only)** |
| `noTimeLimit` | No | Boolean | Assume that we can request an over-ride observation of any length **(test mode only)** |
| `schedule` | Yes* | String | A string version of the CABB schedule |
| `scheduleFile` | Yes* | String | The name of the file to read in as a CABB schedule |
| `serverName` | No | String | The name of the webserver to use when sending the request to the web service |
| `serverProtocol` | No | String | The protocol to use when sending the request to the web service |
| `test` | No | Boolean | Set this to True to indicate that this is only a test request |
| `usePreviousFrequencies` | No | Boolean | Should the service try and schedule using the frequencies that were being used at the start time? |

##### apiEndpoint

*This is an optional property.* (**String**)

If you're submitting a request to the ATCA rapid response service, you probably don't
want to change this parameter from the default value `/cgi-bin/obstools/rapid_response/rapid_response_service.py`.

##### authenticationToken

*This is a required property, although you may choose to
specify `authenticationTokenFile` instead.* (**String**)

This parameter needs to be filled with a [JSON Web Token](https://jwt.io) string that the ATCA rapid response
service will recognise as a valid authentication token. You will have been supplied an authentication token
by observatory staff, and this token must be passed back to the service.

Since the authentication token will have been supplied to you as a file, it is recommended that you pass the
token back by specifying the `authenticationTokenFile` parameter, rather than this parameter.

##### authenticationTokenFile

*This is a required property, although you may choose to
specify `authenticationToken` instead.* (**String**)

This parameter needs to be filled with the name of a readable file that contains a
[JSON Web Token](https://jwt.io) string that the ATCA rapid response service will recognise as a valid
authentication token. You will have been supplied an authentication token file by observatory staff, and
if you pass the name of that file to this parameter, the library will read in the file, and automatically fill the
`authenticationToken` parameter with the string contained within.

##### email

*This is a required property.* (**String**)

You must specify an email address, which the over-ride service will use when sending notifications.
This email address must be one of those supplied on the OPAL proposal for your project. This
parameter is more of a security check than a necessary address.

##### emailOnly

*This is an optional property, and is only used for test requests.* (**String**)

While you are testing your over-ride triggering software, you probably won't want to have emails sent to
your entire team and the teams of those projects you would have displaced. Specify an email address in
this parameter, and that will be the only address to receive any notifications from the over-ride
service.

##### maximumLag

*This is an optional property.* (**Float**)

By default, the rapid response service searches for a suitable start time for your schedule
up to 100 hours from the request time. You may limit this search window by specifying here the
maximum lag, in hours, you are interested in. This parameter is here primarily so you can tell
the service not to bother scheduling the over-ride if it can't be done within the specified
time frame.

##### maxTime

*This is an optional property, and is only used for test requests.* (**Float**)

While you are testing, you may want to see what will happen if the service decides to automatically
shorten your schedule. If you set this parameter, in hours, to a duration less than the total duration
of your schedule, the service will need to shorten your schedule.

##### minimumTime

*This is an optional property.* (**Float**)

You may specify here the minimum amount of time, in hours, that must be available to this request
before the service will schedule it. If you don't specify this property, then the service will
need to be able to allocate enough time to observe your entire schedule before it will schedule
the start time (or as much time as you have left for your project allocation, whichever is smaller).

##### nameCalibrator

*This is a required property.* (**String**)

You must specify the name of one calibrator associated with your target, as it appears in your
schedule. This information is necessary so the service can shorten your schedule if required.

##### nameTarget

*This is a required property.* (**String**)

You must specify the name of the target of your over-ride request, as it appears in your schedule.
This information is necessary so it can ensure your target is above the horizon, and so the
schedule can be appropriately shortened if required.

##### noEmail

*This is an optional property, and is only used for test requests.* (**Boolean**)

If set to `True`, in test mode, then no emails will be sent by the service. This option is available
so you can do testing without spamming yourself or members of your team.

##### noScoreLimit

*This is an optional property, and is only used for test requests.* (**Boolean**)

If set to `True`, in test mode, the service will allow your project to over-ride any
project, including Legacy projects. It will still not allow the project to over-ride
maintenance, reconfigures, or CABB time, or if CABB is not in a suitable mode.

##### noTimeLimit

*This is an optional property, and is only used for test requests.* (**Boolean**)

If set to `True`, in test mode, the service will ignore the amount of time available
to your project when scheduling your over-ride.

##### schedule

*This is a required property, although you may choose to specify `scheduleFile` instead.* (**String**)

This parameter needs to be filled with a string representation of your schedule file.
This is easily achieved from the result of the `toString()` method of the
[CABB Scheduler API](https://github.com/ste616/cabb-schedule-api).

##### scheduleFile

*This is a required property, although you may choose to specify `schedule` instead.* (**String**)

This parameter needs to be filled with the name of readable file that contains your
CABB schedule. The library will read in the file, and automatically fill the
`schedule` parameter with the string version of the schedule.

##### serverName

*This is an optional parameter, and we recommend you not specify it.* (**String**)

This parameter specifies the name of the web server to send your over-ride request to.
By default, this is set to the correct web server for the ATCA rapid response service,
so there is no need to specify anything different.

##### serverProtocol

*This is an optional parameter, and we recommend you not specify it.* (**String**)

This parameter specifies the protocol to use when sending your over-ride request.
By default, this is set to `https://`, and we recommend that you leave this as is.

##### test

*This is an optional parameter.* (**Boolean**)

If set to `True`, the request will treated as a test and will actually be able to
be allocated any telescope time.

##### usePreviousFrequencies

*This is an optional parameter.* (**Boolean**)

Although you must specify frequencies in your schedule, you can tell the service to
replace those frequencies by those configured on the ATCA at the time your schedule
starts. To do this, set this parameter to `True`. Your request is conditional though,
as the service will not change your schedule's frequencies if:
* the band configured at start time is either 7mm or 3mm (ie. the frequency is greater than
30000 MHz),
* the configuration at start time is split between any two bands,
* the configuration is not deemed to be reliable, which occurs if the project C999 is
currently observing, or was the last project that was observed.

#### API methods

The following methods are available on a successfully initialised `rapidRequest` object.

| Method | Description |
| --- | --- |
| `send` | Send the request to the rapid response server, and optionally parse the return value |

##### send

**Arguments**

This method accepts an optional dictionary, which controls how the method parses the
return value from the service.

This dictionary has the following supported properties.

| Property | Required? | Type | Description |
| --- | --- | --- | --- |
| `printSummary` | No | Boolean | Make the method print to the screen a human-readable summary of the return value. |

**Return Value**

This method returns the JSON from the service, although it is presented as a Python
dictionary.




