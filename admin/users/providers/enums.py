from enum import Enum
from .google import GoogleAuthAPI


class Providers(Enum):
    GOOGLE = {
        'provider': GoogleAuthAPI.provider,
        'api': GoogleAuthAPI
    }
