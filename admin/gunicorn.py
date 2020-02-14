import gevent.monkey
gevent.monkey.patch_all()

from multiprocessing import cpu_count

from common.constants import ENV, Envs


def max_workers():
    return cpu_count()


bind = '0.0.0.0:8061'
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()

env = {
    'DJANGO_SETTINGS_MODULE': 'admin.settings'
}

reload = ENV == Envs.Test
name = 'admin'
