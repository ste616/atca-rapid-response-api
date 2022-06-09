# ATCA Rapid Response API
# Python library
# Jamie.Stevens@csiro.au

from requests import Session
import requests
requests.packages.urllib3.disable_warnings()
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
        self.requestDict = None
        self.requestString = None
        if "requestDict" in options:
            self.requestDict = options["requestDict"]

        # The location of the API endpoint.
        self.serverProtocol = "https://"
        self.serverName = "www.narrabri.atnf.csiro.au"
        self.apiEndpoint = "/cgi-bin/obstools/rapid_response/rapid_response_service_dev.py"
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

        # The email address of the requester. This has to be an email address
        # that was supplied in the NAPA proposal.
        self.email = None
        if "email" in options:
            self.email = options['email']

        # And the maximum amount of time in the future we will allow the
        # start time to be, in hours.
        self.maximumLag = None
        if "maximumLag" in options:
            self.maximumLag = options['maximumLag']
            
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
            # Test a particular CABB mode.
            self.testCABBMode = None
            if "testCABBMode" in options:
                self.testCABBMode = options['testCABBMode']
            
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
                print ("Unable to read authentication token file %s, aborting" % self.authenticationTokenFile)
                return None
        if self.authenticationToken is not None:
            data['authToken'] = self.authenticationToken

        if self.maximumLag is not None:
            data['maximumLag'] = self.maximumLag
        
        # The email of the requester.
        data['email'] = self.email

        # Fill in stuff for test mode.
        if self.test == True:
            data['test'] = True
            data['noTimeLimit'] = self.noTimeLimit
            data['noScoreLimit'] = self.noScoreLimit
            if self.emailOnly != "":
                data['emailOnly'] = self.emailOnly
            if self.noEmail == True:
                data['noEmail'] = self.noEmail
            if self.testCABBMode is not None:
                data['testCABBMode'] = self.testCABBMode

        # Fill in all the dictionary stuff.
        #for k in self.requestDict:
        #    data[k] = self.requestDict[k]
        if self.requestDict is not None:
            data["request"] = json.dumps(self.requestDict)
        
        # Send the data.
        print ("sending the following data:")
        print (data)
        print (" -- ")
        url = self.serverProtocol + self.serverName + self.apiEndpoint
        postResponse = session.post( url=url, data=data, verify=False )

        # Parse the JSON that comes back.
        print (postResponse.text)
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
                    print ("Authentication token:")
                    print ("            received: %r" % authToken['received'])
                    print ("            verified: %r" % authToken['verified'])
            else:
                raise responseError("Malformed authentication token response.")
        else:
            raise responseError("Malformed response from server.")

        print ("")

        # We also just return the response object.
        return response
