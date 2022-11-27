import json
import random
import requests
import string
import streamlit as st

def auth(credentials):
	creds = read_creds(credentials)
	print(creds)
	client_id, client_secret = creds['client_id'], creds['client_secret']
	redirect_uri = creds['redirect_uri']
	access_token = creds['access_token']
	return access_token
  
def headers(access_token):
	headers = {
	'Authorization': f'Bearer {access_token}',
	'cache-control': 'no-cache',
	'X-Restli-Protocol-Version': '2.0.0'
	}
	return headers
  
def read_creds(filename):
	with open(filename) as f:
		credentials = json.load(f)
	return credentials

if __name__ == '__main__':
	credentials = 'credentials.json'
	access_token = auth(credentials)
