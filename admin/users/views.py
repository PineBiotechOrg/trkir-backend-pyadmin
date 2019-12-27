import json
import time
import datetime

from django.forms.models import model_to_dict
from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.generate_salt import generate_salt
from common.helpers.get import get
from common.helpers.required_keys import required_keys

from users.providers.constants import Providers
from .helpers.oauth_utils import \
    set_cookie, \
    make_cookie, \
    check_oauth_provider
from .models import Users
from .serializers import UsersSerializer


class UsersViews(viewsets.ModelViewSet):
    serializer_class = UsersSerializer

    @required_keys(['code'])
    def oauth(self, request):  # pylint: disable=unused-argument
        try:
            data = json.loads(request.body)
            code = data.get('code', None)
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

            token_response = provider_api.get_oauth_token(code)
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
                Users.objects.create(login=login, cookies=[cookie])
            else:
                db_user = model_to_dict(db_user)
                db_cookies = db_user['cookies'] if db_user['cookies'] else []
                if cookie not in db_cookies:
                    Users.objects.filter(login=login).update(cookies=db_cookies + [cookie])

            return set_cookie(cookie, expires, {'user': user_info})
        except Exception as e:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)
