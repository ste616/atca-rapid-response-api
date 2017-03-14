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
        self.apiEndpoint = "/cgi-bin/rapid_response/rapid_response_service.py"
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

        # Send the data.
        url = self.serverProtocol + self.serverName + self.apiEndpoint
        postResponse = session.post( url=url, data=data )

        # Parse the JSON that comes back.
        response = json.loads(postResponse.text)
        return response
    
    def send(self, options={}):
        # We've been asked to send the request.
        response = self.__communications()
        if response is None:
            raise preparationError("Could not get all information to send to server.")

        # Go through the returned object and output a summary of what happened.
        if "authenticationToken" in response:
            authToken = response['authenticationToken']
            if "received" in authToken and "verified" in authToken:
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
                            print "      altered: %r (unable to be written to %s)" % (True, outFile)
                        else:
                            print "      altered: %r (written to %s)" % (True, outFile)
                    
            else:
                raise responseError("Malformed schedule response.")
        else:
            raise responseError("Malformed response from server.")

        # We also just return the response object.
        return response
