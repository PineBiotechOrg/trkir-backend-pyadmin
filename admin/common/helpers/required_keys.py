from functools import wraps
import json

from rest_framework import status

from common.helpers.create_custom_response import create_custom_response
from common.helpers.get import get


BAD_KEYS_ERROR = 'Request must contains mandatory keys:'


def required_keys(keys=None):
    if keys is None:
        keys = []

    def wrapper_required_keys(f):
        @wraps(f)
        def decorated_function(view, request, *args, **kwargs):
            data = request.GET \
                if request.method == 'GET' else \
                json.loads(request.body)
            for key in keys:
                try:
                    is_key_exists = get(data, key.split('.'))
                    if is_key_exists is None:
                        return create_custom_response(
                            status.HTTP_400_BAD_REQUEST,
                            {'error': '{} {}'.format(BAD_KEYS_ERROR, ', '.join(keys))},
                        )
                except Exception:
                    return create_custom_response(
                        status.HTTP_400_BAD_REQUEST,
                        {'error': '{} {}'.format(BAD_KEYS_ERROR, ', '.join(keys))},
                    )

            return f(view, request, *args, **kwargs)

        return decorated_function

    return wrapper_required_keys
