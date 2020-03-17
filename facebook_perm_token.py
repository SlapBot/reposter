import requests
from Reposter.utils.information_parser import infoparser
from Reposter.utils.configurer import config


# https://stackoverflow.com/a/28418469
# Make sure to ask for page access token and request publish_pages option when getting the short lived token

# Get page access tokens
def get_access_token_by_page_id(accounts, page_id):
    for account in accounts:
        if account['id'] == page_id:
            return account['access_token']
    return False


def get_long_permanent_token(page_token):
    url = "https://graph.facebook.com/v6.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": page_token
    }
    response = requests.get(url, params=params)
    if not response.ok:
        print(response.text)
        exit("Something bad happened")
    data = response.json()
    long_access_token = data['access_token']
    accound_id_url = "https://graph.facebook.com/v6.0/me"
    response = requests.get(accound_id_url, params={"access_token": long_access_token})
    if not response.ok:
        print(response.text)
        exit("Something bad happened")
    data = response.json()
    account_id = data['id']
    permanent_token_url = "https://graph.facebook.com/v6.0/%s/accounts" % account_id
    requests.get(permanent_token_url, params={"access_token": long_access_token})
    if not response.ok:
        print(response.text)
        exit("Something bad happened")
    return long_access_token


# Initialize parameters
page = "STEPHANIE"
app_id = config.get_configuration("app_id", page)
app_secret = config.get_configuration("app_secret", page)
short_token = config.get_configuration("short_token", page)  # https://developers.facebook.com/tools/explorer

# Get account id
print("Fetching account_id...")
accound_id_url = "https://graph.facebook.com/v6.0/me"
response = requests.get(accound_id_url, params={"access_token": short_token})
if not response.ok:
    print(response.text)
    exit("Something bad happened")
data = response.json()
account_id = data['id']
print(account_id)

print("Fetching page-access-tokens...")
page_access_tokens_url = "https://graph.facebook.com/%s/accounts".format(account_id)
response = requests.get("https://graph.facebook.com/{0}/accounts?access_token={1}".format(
    account_id, short_token
))
if not response.ok:
    print(response.text)
    exit("Something bad happened")
data = response.json()['data']

# Get defined pages from information.json
new_information_data = {'leads': []}
pages = infoparser.get_json_data()['leads']
for page in pages:
    if 'facebook' not in page:
        continue
    page_token = get_access_token_by_page_id(data, page['facebook']['page_id'])
    if page_token:
        long_permanent_token = get_long_permanent_token(page_token)
        new_information_data['leads'].append(
            {
                "facebook": {
                    "name": page['facebook']['name'],
                    "page_id": page['facebook']['page_id'],
                    "token": long_permanent_token,
                    "message": page['facebook']['message']
                },
                "subreddits": page['subreddits']
            }
        )

# Write to information.json
infoparser.write_json_data(new_information_data)
