from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import json
from typing import Generator

CONFIG = None
with open("../config.json") as f:
    CONFIG = json.load(f)

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly" # Only scope needed
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

def _authenticate() -> client.OAuth2Credentials:
    """ Authenticates with the Google Cloud API with 2auth
    
    Returns:
    (client.OAuth2Credentials): 2Oath Credential object
    
    """
    store = file.Storage("./token.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(r"../service_account.json", SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def getResponses() -> Generator[tuple[str, str], None, None]:
    """ Gets all form results as strings 
    
    Returns:
    (Generator[tuple[str, str], None, None]): Yields each response as a tuple with the responseId and its value
    
    """

    creds = _authenticate()
    service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )

    result = service.forms().responses().list(formId=CONFIG['formId']).execute()
    responses = result['responses']
    for response in responses:
        yield (response['responseId'], response['answers']['06b405aa']['textAnswers']['answers'][0]['value'])



if __name__ == "__main__":
    print(list(getResponses()))