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

