# ATCA Rapid Response Service
# Jamie.Stevens@csiro.au

# example3_multifreq.py
# This example script shows how to make a schedule with more than one frequency
# and request time for it from the web service.

# The modules we'll need.
import atca_rapid_response_api as arrApi

# Example 3.
# The situation is the same as in example 1 of the CABB scheduling library example 1.
# Suppose an event trigger has been received for a flaring magnetar at
# coordinates RA = 01:00:43.1, Dec = -72:11:33.8.

rq = { "source": "magnetar", "rightAscension": "08:00:43.1", "declination": "-72:11:33.8",
       "project": "C007", "maxExposureLength": "12:00:00", "minExposureLength": "3:00:00" }

# We want to do a loop of 30 minutes at 4cm, then 30 minutes at 15mm.
rq["4cm"] = { "use": True, "exposureLength": "00:30:00", "freq1": 5500, "freq2": 9000 }
rq["15mm"] = { "use": True, "exposureLength": "00:30:00", "freq1": 17000, "freq2": 19000 }

# We have our request now, so we need to craft the service request to submit it to
# the rapid response service.
rapidObj = { 'requestDict': rq }
# The authentication token needs to go with it, and we point to the file that
# contains the token.
rapidObj['authenticationTokenFile'] = "authorisation_token_test_C007_2022APR.jwt"
# The email address of the requester needs to be there.
rapidObj['email'] = "Jamie.Stevens@csiro.au"

# Because this is a test run, we'll specify a few parameters to just try things out.
rapidObj['test'] = True
rapidObj['emailOnly'] = "Jamie.Stevens@csiro.au"
rapidObj['noScoreLimit'] = True
#rapidObj['noEmail'] = True

# Send the request.
request = arrApi.api(rapidObj)
try:
    response = request.send()
except arrApi.responseError as r:
    print (r.value)


