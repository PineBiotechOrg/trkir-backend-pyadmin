from functools import wraps
import time

from common.constants import influxdb


# TODO: сделать логирование https://tracker.yandex.ru/VPAGROUPDEV-621
def log_view_time():
    def wrapper_log_view_time(f):
        @wraps(f)
        def decorated_function(view, request, *args, **kwargs):
            start = time.time()
            response = f(view, request, *args, **kwargs)
            total = time.time() - start

            try:
                json_body = [
                    {
                        "measurement": "statuses",
                        "fields": {request.method: total}
                    }
                ]
                influxdb.write_points(json_body)
            except:
                # TODO: залогировать ошибку https://tracker.yandex.ru/VPAGROUPDEV-620
                pass

            return response

        return decorated_function

    return wrapper_log_view_time
