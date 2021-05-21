import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize

athelete_activities = "https://www.strava.com/api/v3/athlete/activities"
ldcr_activities= "https://www.strava.com/api/v3/clubs/893517/activities"

def get_access_token():
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': "66259",
        'client_secret': '444ac7af19b35113c5c4cc99a0ef91c6b657cbe0',
        'refresh_token': 'ed3e14f9ad4057c4a2ec261a6472accd79d45ad1',
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))
    return access_token

def get_club_activities(access_token, per_page = 100, pages = 'all'):

    if pages == 'all':
        pages = range(1,100,1)
    if per_page > 200:
        raise ValueError('Number of activities per page must be less than 200.')

    # Read all files in strava_data folder
    data_list = []

    for page in pages:
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page}
        data = requests.get(ldcr_activities, headers=header, params=param).json()
        data = json_normalize(data)

        if data.empty:
            break
        else:
            data_list.append(data)
    
    all_data = pd.concat(data_list, axis=0, ignore_index=True)
    return all_data

def get_athelete_activities(access_token, athelete_id, per_page = 100, pages = 'all'):
    if pages == 'all':
        pages = range(1,100,1)
    if per_page > 200:
        raise ValueError('Number of activities per page must be less than 200.')

    # Read all files in strava_data folder
    data_list = []

    for page in pages:
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page}
        data = requests.get(ldcr_activities, headers=header, params=param).json()
        data = json_normalize(data)

        if data.empty:
            break
        else:
            data_list.append(data)
    
    all_data = pd.concat(data_list, axis=0, ignore_index=True)
    return all_data


def get_user_activities_from_strava(user_dict, start_date_epoch, end_date_epoch):
    # create dictionary of user activities
    activities = {}
    # loop over users
    for user in user_dict:
    ## Get the tokens from file to connect to Strava
        with open('strava_tokens_' + str(user) + '.json') as json_file:
            strava_tokens = json.load(json_file)
            ## If access_token has expired then use the refresh_token to get the new access_token
            if strava_tokens['expires_at'] < time.time():
                #Make Strava auth API call with current refresh token
                response = requests.post(
                                    url = 'https://www.strava.com/oauth/token',
                                    data = {
                                            'client_id': '66259',
                                            'client_secret': '444ac7af19b35113c5c4cc99a0ef91c6b657cbe0',
                                            'grant_type': 'refresh_token',
                                            'refresh_token': strava_tokens['refresh_token']
                                            }
                                )
                #Save response as json in new variable
                new_strava_tokens = response.json()
                # Save new tokens to file
                with open('strava_tokens.json', 'w') as outfile:
                    json.dump(new_strava_tokens, outfile)
                #Use new Strava tokens from now
                strava_tokens = new_strava_tokens
            #Loop through all activities
            page = 1
            url = "https://www.strava.com/api/v3/activities"
            access_token = strava_tokens['access_token']

        ## Create the dataframe ready for the API call to store your activity data
        user_activities = pd.DataFrame(
            columns = [
                    "id",
                    "name",
                    "start_date_local",
                    "type",
                    "distance",
                    "moving_time",
                    "elapsed_time",
                    "total_elevation_gain"
            ]
        )
        while page < 2: # this is to limit the results coming back just in case a user has hundreds of activities in that window
            # get page of activities from Strava
            r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page) + '&after=' + str(start_date_epoch) + '&before=' + str(end_date_epoch))
            r = r.json()
            # if no results then exit loop
            if not r:
                break
        
            # otherwise add new data to dataframe
            for x in range(len(r)):
                user_activities.loc[x + (page-1)*200,'id'] = r[x]['id']
                user_activities.loc[x + (page-1)*200,'name'] = r[x]['name']
                user_activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
                user_activities.loc[x + (page-1)*200,'type'] = r[x]['type']
                user_activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
                user_activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
                user_activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
                user_activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            # increment page
            page += 1

            # add user_activities df to activities dictionary
            activities[user] = user_activities
    return activities


if __name__ == "__main__":
    access_token = get_access_token()
    data = get_club_activities(access_token)
   # data['start_date_local'] = pd.to_datetime(data['start_date_local'])
    print(data)
