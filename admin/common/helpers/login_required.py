from functools import wraps
from datetime import datetime

from rest_framework import status


from common.constants import COOKIE_NAME, TRKIR_UUID_NAME
from common.helpers.generate_salt import generate_salt
from common.helpers.create_custom_response import create_custom_response
from users.helpers.oauth_utils import check_cookie, get_cookie_expires_date_from_seconds


def login_required():
    def wrapper_login_required(f):
        @wraps(f)
        def decorated_function(view, request, *args, **kwargs):
            cookie = request._request.COOKIES.get(COOKIE_NAME, '')
            decrypted_cookie, user = check_cookie(cookie)

            if user is None:
                response = create_custom_response(
                    status.HTTP_401_UNAUTHORIZED,
                    {'reason': 'auth is required'}
                )
                if not request._request.COOKIES.get(TRKIR_UUID_NAME):
                    response.set_cookie(TRKIR_UUID_NAME, generate_salt())

                return response

            expires_date = get_cookie_expires_date_from_seconds(decrypted_cookie['expires'])
            # TODO: Проверить токен google на expires и сделать refresh google токена,
            # если истекает срок жизни (~ < 2 дней)
            # TODO: Написать тесты на проверку даты
            if expires_date < datetime.now():
                response = create_custom_response(
                    status.HTTP_401_UNAUTHORIZED,
                    {'reason': 'cookie is expired'}
                )
                response.set_cookie(COOKIE_NAME, '', expires=0)

                return response

            params = {
                'decrypted_cookie': decrypted_cookie,
                'cookie': cookie,
                'user_info': user,
            }
            return f(view, request, *args, **kwargs, user=params)

        return decorated_function

    return wrapper_login_required
