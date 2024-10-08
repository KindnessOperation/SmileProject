from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import googleapiclient.errors
from typing import Generator
import logging
import time
import sys


logger = logging.getLogger("form")

class Form:
    def __init__(self, formId: str) -> None:
        self.formId = formId
        self.SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly" # Only scope needed
        self.DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    def _authenticate(self) -> client.OAuth2Credentials:
        """ Authenticates with the Google Cloud API with 2auth
        
        Returns:
        (client.OAuth2Credentials): 2Oath Credential object
        
        """
        store = file.Storage("./config/token.json")
        creds = store.get()
        if not creds:
            logger.warning("2OAuth token not found - Manual intervention required")
            flow = client.flow_from_clientsecrets(r"./config/client_secrets.json", self.SCOPES)
            creds = tools.run_flow(flow, store)
            logger.info("OAuth2 Credentials Saved")
            sys.exit(0)
        if creds.invalid:
            logger.warning("Token invalid: Refreshing with client_secrets.json")
            time.sleep(60) # Sleep for 60 seconds to not trip any ratelimit errors
            return self._authenticate()
        return creds

    def getResponses(self) -> Generator[tuple[str, str], None, None]:
        """ Gets all form results as strings 

        Returns:
        (Generator[tuple[str, str], None, None]): Yields each response as a tuple with the responseId and its value
        
        """

        creds = self._authenticate()
        service = discovery.build(
            "forms",
            "v1",
            http=creds.authorize(Http()),
            discoveryServiceUrl=self.DISCOVERY_DOC,
            static_discovery=False,
        )
        try:
            result = service.forms().responses().list(formId=self.formId).execute()
        except googleapiclient.errors.HttpError as error:
            logger.warning("Error occurred when trying to fetch responses: %s" % error)
            time.sleep(5)
            return self.getResponses()
        
        responses = result['responses']
        for response in responses:
            answerKey = list(response['answers'].keys())[0]
            yield (response['responseId'], response['answers'][answerKey]['textAnswers']['answers'][0]['value'])
            
    def getResponse_pks(self) -> list:
        """ Returns a list of response ids used for initialization

        Returns:
        (list): List of response ids
        
        """
        responses = list(self.getResponses())
        return [response[0] for response in responses] # Parse and pick out the responseId and put into a list

if __name__ == "__main__":
    Form("")._authenticate()