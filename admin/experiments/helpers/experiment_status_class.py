from enum import Enum


class ExperimentStatus(Enum):
    CREATED = 'created'
    ACTIVE = 'active'
    PAUSE = 'pause'
    COMPLETED = 'completed'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)