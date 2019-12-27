import os
from enum import Enum


from rest_framework import status

from influxdb import InfluxDBClient

INFLUXDB_HOST = os.getenv('INFLUXDB_HOST')
INFLUXDB_PORT = os.getenv('INFLUXDB_PORT')
INFLUXDB_USER = os.getenv('INFLUXDB_USER')
INFLUXDB_PASS = os.getenv('INFLUXDB_PASS')
INFLUXDB_NAME = os.getenv('INFLUXDB_NAME')
try:
    influxdb = InfluxDBClient(
        host=INFLUXDB_HOST,
        port=INFLUXDB_PORT,
        username=INFLUXDB_USER,
        password=INFLUXDB_PASS
    )
    influxdb.switch_database(INFLUXDB_NAME)
except Exception:
    # TODO: залогировать ошибку https://tracker.yandex.ru/VPAGROUPDEV-620
    pass


# ENV
class Envs(Enum):
    Test = 'TEST'
    Stable = 'STABLE'


ENV = os.environ.get('ENV', Envs.Test.value)


# Roles
ROLE_ADMIN = 'admin'

# common
COOKIE_NAME = 'trkir_auth_cookie'
TRKIR_UUID_NAME = 'trkir_uuid'
DAYDATE_FORMAT = '%d/%m/%Y'

RESPONSES = {
    'DEFAULT': {
        'json': {'message': 'ok'}
    },
    status.HTTP_200_OK: {
        'json': {'message': 'ok'}
    },
    status.HTTP_201_CREATED: {
        'json': {'message': 'ok'}
    },
    status.HTTP_400_BAD_REQUEST: {
        'json': {'message': 'client error', 'reason': 'bad request'}
    },
    status.HTTP_401_UNAUTHORIZED: {
        'json': {'message': 'client error', 'reason': 'unauthorized'}
    },
    status.HTTP_403_FORBIDDEN: {
        'json': {'message': 'client error', 'reason': 'forbidden'}
    },
    status.HTTP_404_NOT_FOUND: {
        'json': {'message': 'client error', 'reason': 'not found'}
    },
    status.HTTP_405_METHOD_NOT_ALLOWED: {
        'json': {'message': 'client error', 'reason': 'method not allowed'}
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        'json': {'message': 'error'}
    },
}
