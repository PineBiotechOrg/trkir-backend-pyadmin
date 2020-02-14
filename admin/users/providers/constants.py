from common.helpers.generate_salt import generate_salt
from .google import GoogleAuthAPI


OAUTH_KEY_FOR_DES = GoogleAuthAPI.client_id[0:4] + GoogleAuthAPI.client_secret[2:6] \
    if GoogleAuthAPI.client_id and GoogleAuthAPI.client_secret else \
    generate_salt()[: 8]

