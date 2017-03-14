# ATCA Rapid Response API
# Python library
# Jamie.Stevens@csiro.au

from requests import Session
import json

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
                return
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
                return
        if self.schedule is not None:
            data['schedule'] = self.schedule

        # Send the data.
        url = self.serverProtocol + self.serverName + self.apiEndpoint
        postResponse = session.post( url=url, data=data )

        # Parse the JSON that comes back.
        response = json.loads(postResponse.text)
        return response
    
