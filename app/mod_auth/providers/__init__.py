from flask_oauth import OAuth

provider_id = {
    'FACEBOOK': 1,
    'TWITTER': 2,
    'GOOGLE': 3
}

oauth = OAuth()
facebook = oauth.remote_app(
    name='facebook',
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://facebook.com/dialog/oauth',
    consumer_key='273840802804076',
    consumer_secret='41480f4a41cdcb5d08d2c10d68795421',
    request_token_params={'scope': 'public_profile, email'}
)

twitter = oauth.remote_app(
    name='twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1.1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authorize',
    # the consumer keys from the twitter application registry.
    consumer_key='xBeXxg9lyElUgwZT6AZ0A',
    consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk'
)

google = oauth.remote_app(
    name='google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key='734224746159-tdqotge1i3hqu1t7aifi62p8komv2l2i.apps.googleusercontent.com',
    consumer_secret='697NMzcRFJsBQPRqdRZOXS9W'
)

import controller_facebook_login, \
       controller_google_login
