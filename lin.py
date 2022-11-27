import requests
import json
from urllib.parse import urlparse, parse_qs
import secrets
from ln_oauth import auth, headers


credentials = 'credentials.json'
access_token = auth(credentials)
headers = headers(access_token)

print(headers)


def user_info():
  response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
  user_info = response.json()
  return user_info['id']

def feed_api():
  l = []
  api_url = 'https://api.linkedin.com/v2/activityFeeds?q=networkShares&count=50'
  response = requests.get(api_url, headers = headers)
  response = response.json()
  print(response)
  for i in response["elements"]:
    l+= [i["reference"]]
  return l

def repost(n, message = ''):
  api_url = 'https://api.linkedin.com/v2/ugcPosts'
  author = f'urn:li:person:{user_info}'
  post_data = { "author": author,
  "commentary": '"' + message + '"',
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false,
  "reshareContext": {
    "parent": n
  }
}
  requests.post(api_url, headers=headers, json=post_data)
  return 

def react(n, typ = "LIKE"):
  api_url = 'https://api.linkedin.com/v2/ugcPosts'
  author = f'urn:li:person:{user_info}'
  post_data = {
    "root": tot_like_cmmt(n)[2],
    "reactionType": f"{typ}"
}
  requests.post(api_url, headers=headers, json=post_data)
  return 

def tot_like_cmmt(n: str):
  link = 'https://api.linkedin.com/rest/socialActions/'+get_urn(n)
  response = requests.get(link, headers = hd())
  response = response.json()
  return [response["commentsSummary"]["aggregatedTotalComments"], response["likesSummary"]["totalLikes"], response["$URN"]]

def get_desc_title(n: str):
  api_url = 'https://api.linkedin.com/v2/activityFeeds?q=networkShares&after=' + str(n) + '&count=1&projection=(paging,elements*(reference~))&quot'
  response = requests.get(api_url, headers = hd())
  response = response.json()
  return [response["contentEntities"]["description"], response["contentEntities"]["title"], response["created"]["actor"]]

def get_id(n: str):
  n = get_desc_title(n)[2]
  n = str(n)
  if 'urn:li:sponsoredAccount:' in n:
    n = n[len('urn:li:sponsoredAccount:'):]
  if 'urn:li:organization:' in n:
    n = n[len('urn:li:organization:'):]
  if 'urn:li:person:' in n:
    n = n[len('urn:li:person:'):]
    
  api_url = 'https://api.linkedin.com/v2/people/id='+ str(n) + '?projection=(id,localizedFirstName,localizedLastName)'
  response = requests.get(api_url, headers = hd())
  response = response.json()
  return response["localizedFirstName"] + " " + response["localizedLastName"]

def comm(n: str, message = 'Thanks for sharing'):
  api_url = "https://api.linkedin.com/rest/socialActions/" + get_urn(n) + "/comments"
  author = f'urn:li:person:{user_info}'
  data = {
   "actor":author,
   "object":n,
   "message":{
      "text":message
   }
  }
  requests.post(api_url, headers=headers, json=data)
  return 

