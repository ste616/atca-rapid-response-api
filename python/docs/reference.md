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
| `schedule` | Yes* | A string version of the CABB schedule |
| `scheduleFile` | Yes* | The name of the file to read in as a CABB schedule |


##### schedule

*This is a required property, although you may choose to
specify `scheduleFile` instead.*

