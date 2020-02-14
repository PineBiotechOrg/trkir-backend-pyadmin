import numpy as np

from analysis.constants.enums import NormalizationMethods


def transform_list_of_dicts_to_dict_of_lists(list_of_dicts, keys=None):
    if keys is None:
        keys = list_of_dicts[0].keys()

    return {
        key: [
            list_dict[key]
            for list_dict in list_of_dicts
        ]
        for key in keys
    }


def transform_dict_of_lists_to_list_of_dicts(dict_of_lists):
    return [
        dict(zip(dict_of_lists, dict_list))
        for dict_list in zip(*dict_of_lists.values())
    ]


def sparse_list(data_list, sparse_value):
    return data_list[::sparse_value]


def moving_average_list(data_list, window_size):
    data_cumsum = np.cumsum(np.insert(data_list, 0, 0), dtype=float)
    return (
            (data_cumsum[window_size:] - data_cumsum[:-window_size]) / float(window_size)
    ).tolist()


def normalize_list(data_list, method):
    max_value = np.max(data_list)
    min_value = np.min(data_list)

    if method == NormalizationMethods.MinMax.value:
        subtract_value = min_value
    if method == NormalizationMethods.Mean.value:
        subtract_value = np.mean(data_list)

    return ((np.array(data_list) - subtract_value) / (max_value - min_value)).tolist()


def find_unique_days_indexes(date_list):
    unique_day_indexes = [0]
    for index in range(1, len(date_list)):
        if date_list[index].day != date_list[unique_day_indexes[-1]].day:
            unique_day_indexes.append(index)

    # need for correct splitting
    unique_day_indexes.append(len(date_list))

    return unique_day_indexes


def split_list_by_indexes(data_list, indexes):
    return [
        data_list[indexes[ind]: indexes[ind + 1]]
        for ind in range(0, len(indexes) - 1)
    ]


def average_lists_to_list(data_lists):
    # need for equal length for all lists
    min_list_length = min([len(data_list) for data_list in data_lists])

    return np.mean(
        [data_list[:min_list_length] for data_list in data_lists],
        axis=0
    ).tolist()
