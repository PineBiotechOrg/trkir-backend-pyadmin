import os
import requests


class GoogleAuthAPI:
    provider = 'google'
    client_id = os.getenv('GOOGLE_APP_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_APP_CLIENT_SECRET')
    info_host = 'https://www.googleapis.com/oauth2/v1'
    token_host = 'https://www.googleapis.com/oauth2/v4/token'

    @staticmethod
    def get_oauth_token(code, redirect_url):
        return requests.post(
            GoogleAuthAPI.token_host,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'client_id': GoogleAuthAPI.client_id,
                'client_secret': GoogleAuthAPI.client_secret,
                'redirect_uri': redirect_url,
                'grant_type': 'authorization_code',
                'code': code,
            }
        ).json()

    @staticmethod
    def get_user_info(token):
        return requests.get(
            '{host}/userinfo?access_token={token}'.format(
                host=GoogleAuthAPI.info_host,
                token=token
            ),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
