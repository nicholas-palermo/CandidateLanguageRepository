# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
#To add wait time between requests
import time

os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFnOjQEAAAAADdXUwAZtYrfekUqXqLaA4blB7IQ%3Dd693MUKg2zJQWQQpIhpQ9CanMCQ5YAzdkTC4kLiWeCVGUDAx8y'

def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(user_Id, start_date, end_date, max_results):
    
    search_url = "https://api.twitter.com/2/users/"+ str(user_Id) +"/tweets" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'until_id': {},
                    'expansions': '',
                    'tweet.fields': 'text',
                    'user.fields': 'id,name,username',
                    'pagination_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, pagination_token):
    params['pagination_token'] = pagination_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def tweetsToFile(candidate, json_response):
    directory = '/Users/nicholas.palermo/Desktop/CSC450/candidateTweets/' + candidate

    with open(directory + '/' + candidate + '-tweets.JSON', 'a') as file:
        #Loop through each tweet
        for tweet in json_response['data']:
            # 1. Tweet Text
            text = tweet['text']
            file.write(text + '\n')

def tweetsToJSON(candidate, json_response):
    directory = '/Users/nicholas.palermo/Desktop/CSC450/candidateTweets/' + candidate
    json_object = json.dumps(json_response, indent=4)

    with open(directory + '/' + candidate + '-tweets.JSON', 'a') as file:
        file.write(json_object)

#Inputs for the request
candidate_ids = {
                'zeldinfornewyork': '2750127259',
                'jamesforny': '132496568',
                'michaelhenryforag': '2551266673',
                'maxroseforcongress': '892491627088011264',
                'nicolemalliotakis': '757862089'
                }



# url = create_url(user_Id, start_time, end_time, max_results)
# json_response = connect_to_endpoint(url[0], headers, url[1])

# json_object = json.dumps(json_response, indent=4)

# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)



for candidate, id in candidate_ids.items():
    print('Retrieving Tweets for ' + candidate + "...")
    time.sleep(2)

    bearer_token = auth()
    headers = create_headers(bearer_token)
    user_Id = id
    start_time = "2018-01-01T00:00:00.000Z"
    end_time = "2022-12-31T00:00:00.000Z"
    max_results = 100

    # Inputs
    count = 0 # Counting tweets per time period
    max_count = 3200 # Max tweets per candidate
    flag = True
    pagination_token = None
    until_id = None
    total_tweets = 0

    while flag:

        if count >= max_count:
            break

        print('---------------------------')
        print("Token: ", pagination_token)
        url = create_url(user_Id, start_time, end_time, max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], pagination_token)
        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            pagination_token = json_response['meta']['next_token']
            print("Next Token: ", pagination_token)
            if result_count is not None and result_count > 0 and pagination_token is not None:
                tweetsToFile(candidate, json_response)
                tweetsToJSON(candidate, json_response)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(2)                
        # If no next token exists
        else:
            if result_count is not None and result_count > 0:
                print("-------------------")
                tweetsToFile(candidate, json_response)
                tweetsToJSON(candidate, json_response)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(2)
            
            #Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            pagination_token = None
        time.sleep(5)
        print("Total number of results: ", total_tweets)