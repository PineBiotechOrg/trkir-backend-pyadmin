from enum import Enum


class CameraStatus(Enum):
    ON = 'on'
    OFF = 'off'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
