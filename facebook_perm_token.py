import requests
from Reposter.utils.configurer import config

# https://stackoverflow.com/a/28418469
# Make sure to ask for page access token and request publish_pages option when getting the short lived token

page = "STEPHANIE"

app_id = config.get_configuration("app_id", page)
app_secret = config.get_configuration("app_secret", page)
short_token = config.get_configuration("short_token", page)

url = "https://graph.facebook.com/v2.10/oauth/access_token"

params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": short_token
}

response = requests.get(url, params=params)

if not response.ok:
    print(response.text)
    exit("Something bad happened")

data = response.json()

long_access_token = data['access_token']
print(long_access_token)

config.write_configuration("long_token", long_access_token, page)

accound_id_url = "https://graph.facebook.com/v2.10/me"

response = requests.get(accound_id_url, params={"access_token": long_access_token})

if not response.ok:
    print(response.text)
    exit("Something bad happened")

data = response.json()

account_id = data['id']
print(account_id)

permanent_token_url = "https://graph.facebook.com/v2.10/%s/accounts" % account_id

requests.get(permanent_token_url, params={"access_token": long_access_token})

if not response.ok:
    print(response.text)
    exit("Something bad happened")

