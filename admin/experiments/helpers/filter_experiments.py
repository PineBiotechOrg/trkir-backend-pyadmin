from common.helpers.models_to_list import models_to_list


def filter_experiments(experiments, filters):
    # TODO: сделать фильтрацию экспериментов https://tracker.yandex.ru/VPAGROUPDEV-601
    return models_to_list(experiments)
