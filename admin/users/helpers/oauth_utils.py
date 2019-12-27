import base64
import datetime
from Crypto.Cipher import DES

from django.forms.models import model_to_dict
from rest_framework import status

from common.helpers.create_custom_response import create_custom_response
from common.constants import COOKIE_NAME
from users.models import Users
from users.providers.constants import Providers, OAUTH_KEY_FOR_DES


def check_oauth_provider(provider):
    provider_api = None
    for access_provider in Providers:
        if access_provider.value['provider'] == provider:
            provider_api = access_provider.value['api']
            break

    return provider_api


def padding_text(text):
    while len(text) % 8 != 0:
        text += b' '

    return text


def encrypt(text):
    # Надо ли делать это один раз в проекте?
    # Но тогда кажется может быть компроментация данных и только перезапуском приложения можно все исправить
    # + может быть гонка на str.encode(oauth_key_for_des())
    des = DES.new(str.encode(OAUTH_KEY_FOR_DES), DES.MODE_ECB)
    padded_text = padding_text(text)
    return base64.b64encode(des.encrypt(padded_text)).decode('utf-8')


def decrypt(text):
    # Надо ли делать это один раз в проекте?
    # Но тогда кажется может быть компроментация данных и только перезапуском приложения можно все исправить
    # + может быть гонка на str.encode(oauth_key_for_des())
    des = DES.new(str.encode(OAUTH_KEY_FOR_DES), DES.MODE_ECB)
    decoded = base64.b64decode(str.encode(text))
    padded_text = padding_text(decoded)
    return des.decrypt(padded_text)


def make_cookie(data=None):
    if data is None:
        data = []
    return base64. \
        b64encode(str.encode(':'.join([encrypt(str.encode(token)) for token in data]))). \
        decode('utf-8')


def decrypt_cookie(target):
    if target is None:
        return None

    decoded_cookie = base64.b64decode(str.encode(target)).decode('utf-8')
    splitted = decoded_cookie.split(':')
    decrypted_data = [decrypt(target).decode('utf-8').strip() for target in splitted]

    return {
        'login': decrypted_data[0],
        'expires': decrypted_data[2],
    }


def check_cookie(cookie):
    try:
        user = model_to_dict(Users.objects.filter(cookies__contains=[cookie])[0])
        user_cookies_info(user).index(cookie)

        return decrypt_cookie(cookie), user
    except Exception as e:
        return None, None


def user_cookies_info(user):
    if 'cookies' in user.keys():
        cookies = user['cookies']
        return cookies if type(cookies) == list else [cookies]

    return []


def delete_cookie(login, cookie):
    if not login or not cookie:
        return

    user = model_to_dict(Users.objects.get(login=login))

    new_cookies = user['cookies'].remove(cookie)
    Users.objects.filter(login=login).update(cookies=new_cookies)


def get_cookie_expires_date_from_seconds(target):
    return datetime.datetime.fromtimestamp(int(float(target)))


def set_cookie(cookie, expires, data=None):
    if data is None:
        data = {}
    response = create_custom_response(
        status.HTTP_200_OK,
        data
    )
    response.set_cookie(COOKIE_NAME, cookie, expires=expires)

    return response
