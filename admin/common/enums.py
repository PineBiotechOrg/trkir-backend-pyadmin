from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((data.name, data.value) for data in cls)

    @classmethod
    def validate(cls, value):
        for data in cls:
            if value == data.value:
                return True

        return False

    @classmethod
    def choices_to_json(cls):
        return [
            {'value': data[1], 'label': data[0]}
            for data in cls.choices()
        ]

    @classmethod
    def get_values_list(cls):
        return [field.value for field in cls]
