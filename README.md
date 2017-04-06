# atca-rapid-response-api
API to submit requests for the ATCA rapid response mode.

The [Australia Telescope Compact Array](https://www.narrabri.atnf.csiro.au) has the ability to very quickly
respond to requests to observe transient events. All requests need to be submitted via the web service
provided by the observatory, and this API is supplied to make this process easy.

As much of the code that transient astronomers use to receive, parse and react to events is written in
Python, the [Python](python) library is recommended. The library functions may be made available in
other languages if there is sufficient demand.

