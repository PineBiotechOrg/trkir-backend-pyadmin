import json

from django.urls import resolve, reverse

from admin.urls import BASE_URL


def make_request(method, path, body=None, params=None):
    url = '/{base}/{path}/'.format(base=BASE_URL, path=path)

    if body:
        return method(url, json.dumps(body), content_type="application/json")
    elif params:
        return method(url, params)
    else:
        return method(url)


def make_without_dates(data):
    if isinstance(data, list):
        for d in data:
            date_keys = list(filter(lambda x: 'date' in x, d.keys()))
            for key in date_keys:
                del d[key]
    else:
        date_keys = list(filter(lambda x: 'date' in x, data.keys()))
        for key in date_keys:
            del data[key]

    return data
