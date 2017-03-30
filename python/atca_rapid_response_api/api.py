# ATCA Rapid Response API
# Python library
# Jamie.Stevens@csiro.au

from requests import Session
import json

# We have a couple of error classes here.
class responseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class preparationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# The API class gathers all the required information, sends it to the service
# when asked to, and then handles the response from the service.
class api:
    def __init__(self, options):
        # The schedule string, or a pointer to the file with the token.
        # This should come from the cabb_scheduler library.
        self.schedule = None
        self.scheduleFile = None
        if "schedule" in options:
            self.schedule = options['schedule']
        elif "scheduleFile" in options:
            self.scheduleFile = options['scheduleFile']

        # The location of the API endpoint.
        self.serverProtocol = "https://"
        self.serverName = "www.narrabri.atnf.csiro.au"
        self.apiEndpoint = "/cgi-bin/obstools/rapid_response/rapid_response_service.py"
        if "serverProtocol" in options:
            self.serverProtocol = options['serverProtocol']
        if "serverName" in options:
            self.serverName = options['serverName']
        if "apiEndpoint" in options:
            self.apiEndpoint = options['apiEndpoint']
        
        # The authentication token we were provided with, or a pointer to the
        # file with the token.
        self.authenticationToken = None
        self.authenticationTokenFile = None
        if "authenticationToken" in options:
            self.authenticationToken = options['authenticationToken']
        elif "authenticationTokenFile" in options:
            self.authenticationTokenFile = options['authenticationTokenFile']

        # The name of the main target in the schedule.
        self.nameTarget = None
        if "nameTarget" in options:
            self.nameTarget = options['nameTarget']
        # And the first calibrator for that target.
        self.nameCalibrator = None
        if "nameCalibrator" in options:
            self.nameCalibrator = options['nameCalibrator']

        # The email address of the requester. This has to be an email address
        # that was supplied in the NAPA proposal.
        self.email = None
        if "email" in options:
            self.email = options['email']

        # The minimum amount of time that we require on the schedule for the
        # observation to be useful. This should be given in hours.
        self.minimumTime = None
        if "minimumTime" in options:
            self.minimumTime = options['minimumTime']

        # We need to be able to tell the system that we want to use the
        # frequencies of whatever project we over-ride.
        self.usePreviousFrequencies = False
        if "usePreviousFrequencies" in options:
            self.usePreviousFrequencies = options['usePreviousFrequencies']
            
        # Some parameters relating to test mode.
        self.test = False
        if "test" in options:
            self.test = options['test']
        if self.test == True:
            # We can specify other things to test now.
            # Disable the check to see if this project has any time left to schedule.
            self.noTimeLimit = False
            if "noTimeLimit" in options:
                self.noTimeLimit = options['noTimeLimit']
            # Disable the check to see if we have a high-enough score.
            self.noScoreLimit = False
            if "noScoreLimit" in options:
                self.noScoreLimit = options['noScoreLimit']
            # Only send an email to a single email address.
            self.emailOnly = ""
            if "emailOnly" in options:
                self.emailOnly = options['emailOnly']
            # Disable sending an email completely.
            self.noEmail = False
            if "noEmail" in options:
                self.noEmail = options['noEmail']
            
    def __communications(self):
        # This session is how we communicate with the endpoint.
        session = Session()

        # This is the data we send to the endpoint.
        data = {}

        # Include the authentication token.
        if self.authenticationTokenFile is not None:
            # Read in the file.
            try:
                with open(self.authenticationTokenFile, 'r') as atf:
                    self.authenticationToken = atf.readlines()[0].rstrip()
            except IOError:
                print "Unable to read authentication token file %s, aborting" % self.authenticationTokenFile
                return None
        if self.authenticationToken is not None:
            data['authToken'] = self.authenticationToken

        # Include the schedule.
        if self.scheduleFile is not None:
            # Read in the file.
            try:
                with open(self.scheduleFile, 'r') as sf:
                    self.schedule = sf.read()
            except IOError:
                print "Unable to read schedule file %s, aborting" % self.scheduleFile
                return None
        if self.schedule is not None:
            data['schedule'] = self.schedule
        # Send some metadata about the schedule.
        data['nameTarget'] = self.nameTarget
        data['nameCalibrator'] = self.nameCalibrator
        data['minimumTime'] = self.minimumTime
        data['usePreviousFrequencies'] = self.usePreviousFrequencies
        
        # The email of the requester.
        data['email'] = self.email

        # Fill in stuff for test mode.
        if self.test == True:
            data['test'] = True
            data['noTimeLimit'] = True
            data['noScoreLimit'] = True
            if self.emailOnly != "":
                data['emailOnly'] = self.emailOnly
            if self.noEmail == True:
                data['noEmail'] = self.noEmail
        
        # Send the data.
        print "sending the following data:"
        print data
        print " -- "
        url = self.serverProtocol + self.serverName + self.apiEndpoint
        postResponse = session.post( url=url, data=data )

        # Parse the JSON that comes back.
        print postResponse.text
        response = json.loads(postResponse.text)
        return response
    
    def send(self, options={}):
        # We've been asked to send the request.
        response = self.__communications()
        if response is None:
            raise preparationError("Could not get all information to send to server.")
        
        if "printSummary" not in options:
            options['printSummary'] = False


        # Go through the returned object and output a summary of what happened.
        # If there is ever an error, the 'error' parameter will be present in the
        # returned JSON.
        if "error" in response:
            raise responseError(response['error'])

        if "authenticationToken" in response:
            authToken = response['authenticationToken']
            if "received" in authToken and "verified" in authToken:
                if options['printSummary'] == True:
                    print "Authentication token:"
                    print "            received: %r" % authToken['received']
                    print "            verified: %r" % authToken['verified']
            else:
                raise responseError("Malformed authentication token response.")
        else:
            raise responseError("Malformed response from server.")

        print ""

        if "schedule" in response:
            schedule = response['schedule']
            if "received" in schedule and "valid" in schedule and "altered" in schedule:
                if options['printSummary'] == True:
                    print "Schedule file:"
                    print "     received: %r" % schedule['received']
                    print "        valid: %r" % schedule['valid']
                if schedule['altered'] is not None:
                    # Write out the schedule.
                    if self.scheduleFile is not None:
                        outFile = "altered_" + self.scheduleFile
                        try:
                            with open(outFile, 'w') as of:
                                of.write(outFile)
                        except IOError:
                            if options['printSummary'] == True:
                                print "      altered: %r (unable to be written to %s)" % (True, outFile)
                        else:
                            if options['printSummary'] == True:
                                print "      altered: %r (written to %s)" % (True, outFile)
                            response['schedule']['filename'] = outFile
                    
            else:
                raise responseError("Malformed schedule response.")
        else:
            raise responseError("Malformed response from server.")

        # We also just return the response object.
        return response
