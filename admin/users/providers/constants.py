from enum import Enum

from common.helpers.generate_salt import generate_salt
from .google import GoogleAuthAPI


OAUTH_KEY_FOR_DES = generate_salt()[: 8]


class Providers(Enum):
    GOOGLE = {
        'provider': GoogleAuthAPI.provider,
        'api': GoogleAuthAPI
    }

