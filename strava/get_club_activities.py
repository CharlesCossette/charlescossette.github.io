import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token = 'b03dc15ada79445c2e39800f8b7db57c77527d89'

# create an instance of the API class
api_instance = swagger_client.ClubsApi()
id = 789 # Long | The identifier of the club.
page = 56 # Integer | Page number. Defaults to 1. (optional)
perPage = 56 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

try: 
    # List Club Activities
    api_response = api_instance.getClubActivitiesById(id, page=page, perPage=perPage)
    print(api_response)
except ApiException as e:
    print("Exception when calling ClubsApi->getClubActivitiesById: %s\n" % e)