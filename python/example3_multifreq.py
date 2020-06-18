# ATCA Rapid Response Service
# Jamie.Stevens@csiro.au

# example3_multifreq.py
# This example script shows how to make a schedule with more than one frequency
# and request time for it from the web service.

# The modules we'll need.
import atca_rapid_response_api as arrApi
import cabb_scheduler as cabb

# Example 3.
# The situation is the same as in example 1 of the CABB scheduling library example 1.
# Suppose an event trigger has been received for a flaring magnetar at
# coordinates RA = 01:00:43.1, Dec = -72:11:33.8.

# Make a new schedule.
schedule = cabb.schedule()

# Add a scan to look at the magnetar's coordinates.
# This is also where we set our project code; in this example we'll use
# the code C006 (we have a test authorisation token for this project).
# We'll also set it to be 20 minutes long, with Dwell mode.
scan1 = schedule.addScan(
    { 'source': "magnetar", 'rightAscension': "08:00:43.1", 'declination': "-72:11:33.8",
      'freq1': 5500, 'freq2': 9000, 'project': "C006",
      'scanLength': "00:20:00", 'scanType': "Dwell" }
)

# Request a list of nearby calibrators from the ATCA calibrator database.
calList = scan1.findCalibrator()

# Ask for the library to choose the best one for the current array. We first need to
# get the current array from MoniCA.
currentArray = cabb.monica_information.getArray()
# And pass this as the arggument to the calibrator selector.
bestCal = calList.getBestCalibrator(currentArray)
# This should choose 2353-686.
print ("Calibrator chosen: %s, %.1f degrees away" % (bestCal['calibrator'].getName(),
                                                     bestCal['distance']))

# We add this calibrator to the schedule, attaching it to the scan it
# will be the calibrator for. We'll ask to observe the calibrator for 2
# minutes.
calScan = schedule.addCalibrator(bestCal['calibrator'], scan1, { 'scanLength': "00:02:00" })

# Now we add another scan at a different frequency.
scan2 = schedule.addScan(
    { 'source': "magnetar", 'rightAscension': "08:00:43.1", 'declination': "-72:11:33.8",
      'freq1': 17000, 'freq2': 19000, 'project': "C006", 'scanLength': "00:10:00",
      'scanType': "Dwell" }
)
# Find the calibrators.
cal_mm_List = scan2.findCalibrator()
best_mm_Cal = cal_mm_List.getBestCalibrator(currentArray)
print ("MM Calibrator chosen: %s, %.1f degrees away" % (best_mm_Cal['calibrator'].getName(),
                                                        best_mm_Cal['distance']))
cal_mm_Scan = schedule.addCalibrator(best_mm_Cal['calibrator'], scan2, { 'scanLength': "00:02:00" })

# We want the schedule to run for some time, so we want another two copies
# of these scans. Remembering that the library will take care of
# associating a calibrator to each source, we only need to copy the source
# scan.
for i in range(0, 2):
    schedule.copyScans([ scan1.getId() ])
    schedule.copyScans([ scan2.getId() ])

# Tell the library that we won't be looping, so there will be a calibrator scan at the
# end of the schedule.
schedule.setLooping(False)

# Ensure proper focus scans are put in.
schedule.completeSchedule()

# We need to turn this schedule into a string.
schedString = schedule.toString()
# Let's keep a copy.
schedule.write("example3.sch")

# We have our schedule now, so we need to craft the service request to submit it to
# the rapid response service.
rapidObj = { 'schedule': schedString }
# The authentication token needs to go with it, and we point to the file that
# contains the token.
rapidObj['authenticationTokenFile'] = "authorisation_token_test_C006_2020APR.jwt"
# The name of the main target needs to be specified.
rapidObj['nameTarget'] = "magnetar"
# So does the name of the calibrator.
rapidObj['nameCalibrator'] = bestCal['calibrator'].getName()
# The email address of the requester needs to be there.
rapidObj['email'] = "Jamie.Stevens@csiro.au"
# We don't want to use whatever frequencies are running at the time.
rapidObj['usePreviousFrequencies'] = False
# We only ask for times more than 0.2 hours.
rapidObj['minimumTime'] = 0.2

# Because this is a test run, we'll specify a few parameters to just try things out.
rapidObj['test'] = True
rapidObj['emailOnly'] = "Jamie.Stevens@csiro.au"
#rapidObj['noTimeLimit'] = True
rapidObj['maxTime'] = 10
rapidObj['noScoreLimit'] = True
#rapidObj['noEmail'] = True

# Send the request.
request = arrApi.api(rapidObj)
try:
    response = request.send()
except arrApi.responseError as r:
    print (r.value)

# Write out the altered schedule to check what happened to it.
asched = cabb.schedule()
#print ("%s" % response['schedule']['altered'])
asched.parse(response['schedule']['altered'])
asched.write("example3_altered.sch")

