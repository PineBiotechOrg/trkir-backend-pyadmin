import json
import time
import datetime

from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.generate_salt import generate_salt
from common.helpers.get import get
from common.helpers.login_required import login_required
from common.helpers.required_keys import required_keys
from common.constants import COOKIE_NAME

from users.providers.enums import Providers
from users.helpers.oauth_utils import check_cookie
from .helpers.oauth_utils import \
    set_cookie, \
    make_cookie, \
    check_oauth_provider
from .models import Users, Cookies
from .serializers import UsersSerializer


class UsersViews(viewsets.ModelViewSet):
    serializer_class = UsersSerializer

    def get_user_data(self, request):
        try:
            cookie = request._request.COOKIES.get(COOKIE_NAME, '')
            decrypted_cookie, user = check_cookie(cookie)

            if user is None:
                return create_custom_response(
                    status.HTTP_401_UNAUTHORIZED,
                    {'reason': 'auth is required'}
                )

            return create_custom_response(
                status.HTTP_200_OK,
                {'user': user}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'code',
        'redirect_url'
    ])
    def oauth(self, request):  # pylint: disable=unused-argument
        try:
            data = json.loads(request.body)
            code = data.get('code')
            redirect_url = data.get('redirect_url')

            provider = data.get('provider', Providers.GOOGLE.value['provider'])

            if not code:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'No code'},
                )

            provider_api = check_oauth_provider(provider)

            if not provider_api:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'Not valid provider'},
                )

            token_response = provider_api.get_oauth_token(code, redirect_url)

            expires = time.mktime(
                (datetime.datetime.now() + datetime.timedelta(seconds=token_response['expires_in'])).timetuple()
            )
            access_token = token_response['access_token']

            user_info_response = provider_api.get_user_info(access_token)
            if user_info_response.status_code != 200:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'No valid token'},
                )

            user_info = user_info_response.json()
            login = user_info['email']

            cookie = make_cookie(
                [
                    login,
                    generate_salt(),
                    str(expires),
                ]
            )

            db_user = get(list(Users.objects.filter(login=login)), [0])
            if db_user is None:
                db_user = Users.objects.create(login=login)
                Cookies.objects.create(user=db_user, cookie=cookie)
            else:
                user_cookie = Cookies.objects \
                    .filter(user=db_user.id) \
                    .values_list('cookie', flat=True)

                if cookie not in user_cookie:
                    Cookies.objects.create(user=db_user, cookie=cookie)

            return set_cookie(cookie, expires, {'user': user_info})
        except Exception as e:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def logout(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']
            cookie = request._request.COOKIES.get(COOKIE_NAME, '')

            response = create_custom_response(status.HTTP_200_OK)
            response.set_cookie(COOKIE_NAME, '', expires=0)

            Cookies.objects.filter(user_id=user_id, cookie=cookie).delete()

            return response
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def update(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            update_fields = json.loads(request.body)
            Users.objects.filter(pk=user_id).update(
                **update_fields,
            )

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_service_client_id(self, request): # pylint: disable=unused-argument
        try:
            data = request.GET
            provider = data.get('provider', Providers.GOOGLE.value['provider'])

            provider_api = check_oauth_provider(provider)

            if not provider_api:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'Not valid provider'},
                )

            return create_custom_response(
                status.HTTP_200_OK,
                {'client_id': provider_api.client_id}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
