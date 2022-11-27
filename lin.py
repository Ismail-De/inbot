import requests
import json
from urllib.parse import urlparse, parse_qs
import streamlit as st
import secrets

client_id = '86wluahn9m77um'
client_secret = 'Tp9m8CH7oGBklnCq'
redirect_uri = 'https://api-university.com/'


def auth():
  #file = open('token.txt', 'r')
  with open('token.txt') as f:
    first_line = f.readline()
  print(first_line)
  base_url = "https://www.linkedin.com/oauth/v2/authorization&quot"
  scope = "w_member_social,r_liteprofile"
  url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
  if 'access_token' in first_line:
    access_token = first_line[len('access_token: '):]
    access_token = access_token.replace(" ", "")
    access_token = access_token.replace("\n", "")
    print('"'+str(access_token)+'"')
    #file.close()
    return access_token

  else: 
      args = client_id,client_secret,redirect_uri
      st.write("Please visit this" + url)
      with st.form("my_form"):
        title = st.text_input('Paste the full redirect URL here: (Press Submit)')
        submitted = st.form_submit_button("Submit")
      if submitted:
        print(title)
        auth_code = title
        access_token = refresh_token(auth_code)
        #file.close()
        file = open('token.txt', 'w')
        file.write('access_token: ')
        file.write(auth_code)
        file.write('\n')
        file.close()
        print(access_token)
        return access_token


def headers(access_token):
  headers = {
  'Content-Type': 'application/json',
  'X-Restli-Protocol-Version': '2.0.0',
  'Authorization': f'Bearer {access_token}'
  }
  return json.dumps(headers)

def refresh_token(auth_code):
  url_access_token = "https://www.linkedin.com/oauth/v2/accessToken"
  payload = {
      'grant_type' : 'authorization_code',
      'code' : auth_code,
      'redirect_uri' : redirect_uri,
      'client_id' : client_id,
      'client_secret' : client_secret
  }
  response = requests.post(url=url_access_token, json=payload)
  print(response)
  response_json = response.json()
  access_token = response_json['access_token']
  return access_token

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

