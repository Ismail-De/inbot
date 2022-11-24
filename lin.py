import requests
import json
from urllib.parse import urlparse, parse_qs
import streamlit as st
import secrets

client_id = ''
client_secret = ''
redirect_uri = ''


def auth():
  #file = open('token.txt', 'r')
  with open('token.txt') as f:
    first_line = f.readline()
  print(first_line)
  url = requests.Request(
    'GET',
    'https://www.linkedin.com/oauth/v2/authorization',
    params = {
        'response_type': 'code',
        'client_id': 'REPLACE_WITH_YOUR_CLIENT_ID',
        'redirect_uri': 'REPLACE_WITH_REDIRECT_URL',
        'state': secrets.token_hex(8).upper(),
        'scope': ' '.join(['r_liteprofile', 'r_emailaddress', 'w_member_social']),
    },
).prepare().url
  st.write(url)
  if 'access_token' in first_line:
    access_token = first_line[len('access_token: '):]
    access_token = access_token.replace(" ", "")
    access_token = access_token.replace("\n", "")
    print('"'+str(access_token)+'"')
    print(access_token, client_id,client_secret,redirect_uri)
    #file.close()
    return refresh_token(access_token, client_id, client_secret, redirect_uri)

  else: 
      args = client_id,client_secret,redirect_uri
      st.write(authoriz(client_id,client_secret,redirect_uri))
      #title = st.text_input('Paste the full redirect URL here: (Press Enter)')
      with st.text_input('Paste the full redirect URL here: (Press Enter)'):
        auth_code = authorize(title)
        access_token = refresh_token(auth_code,*args)
        #file.close()
        file = open('token.txt', 'w')
        file.write('access_token: ')
        file.write(access_token)
        file.write('\n')
        file.close()
        print(access_token)
        return access_token

def authoriz(client_id,client_secret,redirect_uri):
  api_url = 'https://www.linkedin.com/oauth/v2'
  params = {
      'response_type': 'code',
      'client_id': client_id,
      'redirect_uri': redirect_uri,
      'scope': 'r_liteprofile,r_emailaddress,w_member_social'
      }

  response = requests.get(f'{api_url}/authorization',params=params)
  s = "Please go here and authorize:" + str(response.url)
  return s

def parse_redirect_uri(redirect_response):
  ind = redirect_response.index('code=')
  return ind[ind+len('code='):]

def authorize(mm):
  auth_code = parse_redirect_uri(mm)
  return auth_code

def headers(access_token):
  headers = {
  'Authorization': f'Bearer {access_token}',
  'cache-control': 'no-cache',
  'x-li-src':'msdk',
  'X-Restli-Protocol-Version': '2.0.0',
  }
  return json.dumps(headers)

def refresh_token(auth_code,client_id,client_secret,redirect_uri):
  access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
  hh = {'ContentType': 'application/x-www-form-urlencoded'}
  access_token = requests.post(
    'https://www.linkedin.com/oauth/v2/accessToken',
    params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': 'REPLACE_WITH_REDIRECT_URL',
        'client_id': 'REPLACE_WITH_YOUR_CLIENT_ID',
        'client_secret': 'REPLACE_WITH_YOUR_CLIENT_SECRET',
    },
).json()
  print(access_token)
  return access_token['access_token']

def hd():
  access_token = auth()
  hds = headers(access_token)
  return hds

def user_info():
  response = requests.get('https://api.linkedin.com/v2/me', headers = hd())
  user_info = response.json()
  return user_info['id']

def feed_api():
  l = []
  api_url = 'https://api.linkedin.com/v2/activityFeeds?q=networkShares&count=50'
  with st.button('Start'):
    response = requests.get(api_url, headers = hd())
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
  response = requests.get('https://api.linkedin.com/v2/me', headers = hd())
  response = response.json()
  return [response["commentsSummary"]["aggregatedTotalComments"], response["likesSummary"]["totalLikes"], response["$URN"]]

def get_desc_title(n: str):
  api_url = 'https://api.linkedin.com/v2/activityFeeds?q=networkShares&after=' + str(n) + '&count=1&projection=(paging,elements*(reference~))'
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
