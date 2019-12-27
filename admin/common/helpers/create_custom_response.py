from rest_framework import status
from django.http import JsonResponse

from common.constants import RESPONSES

from .get import get


def create_custom_response(code=status.HTTP_200_OK, data=None):
    if data is None:
        data = {}

    response_json = get(RESPONSES, [code, 'json'])

    if response_json is None:
        return JsonResponse({**get(RESPONSES, ['DEFAULT', 'json']), **data}, status=code)

    return JsonResponse({**response_json, **data}, status=code)
