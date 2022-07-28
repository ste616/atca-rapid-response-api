# ATCA Rapid Response Service
# Jamie.Stevens@csiro.au

# example4_cancel.py
# This example script shows how to request a cancellation of a previously-submitted
# trigger.

# The modules we'll need.
import atca_rapid_response_api as arrApi
import json

# Example 4.
# We've requested that the ATCA rapid resposne service observe something, but now
# we want to kill that request.
# When we made the request, we got the following message back:
retval = '{"authenticationToken": {"received": true, "verified": true}, "overrideProject": {"code": "C007", "sufficientScore": true, "score": 5.0}, "scheduledProject": {"codes": ["C001", "DT"], "emails": [["s.person@anemailaddress.com", "a.person@anemailaddress.com.au"], ""], "startTimes": [44754.47916666667, 0], "endTimes": [44754.9375, 0]}, "schedule": {"received": true, "valid": true, "targetName": "magnetar", "rightAscension": "08:00:43.1", "declination": "-72:11:33.8", "bandsRequested": ["4cm", "15mm"], "4cm": {"use": true, "exposureLength": "00:30:00", "freq1": 5500, "freq2": 9000}, "15mm": {"use": true, "exposureLength": "00:30:00", "freq1": 17000, "freq2": 19000}}, "observations": {"hoursRequested": 12.0, "maxSearchHours": 100, "hoursAllocated": 12.0, "hoursRequestedMinimum": 3.0, "projectHoursRemaining": 132.0, "startDate": "2022-07-14 04:56:50", "endDate": "2022-07-14 16:56:50"}, "testMode": false, "cancel": false, "testing": {"noScoreLimit": false, "noTimeLimit": false, "limitTimeHours": 0, "CABBMode": "ca_2048_2048_2f"}, "id": "s25fufcqy45l5m72fbjv", "success": true}'
# We need to parse this return value.
retObj = json.loads(retval)

# We have the ID in that package.
cancelId = retObj['id']

# We craft the request now.
rapidObj = { 'requestDict': { 'cancel': cancelId, 'project': "C007" } }
# The authentication token needs to be valid for the cancellation request
# to work.
rapidObj['authenticationTokenFile'] = "authorisation_token_test_C007_2022APR.jwt"
# The email address of the requester needs to be there.
rapidObj['email'] = "Jamie.Stevens@csiro.au"

# Send the request.
request = arrApi.api(rapidObj)
try:
    response = request.send()
except arrApi.responseError as r:
    print (r.value)
    
