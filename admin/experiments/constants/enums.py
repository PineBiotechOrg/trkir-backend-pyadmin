from common.enums import ChoicesEnum


class ExperimentStatuses(ChoicesEnum):
    Create = 'create'
    Start = 'start'
    Pause = 'pause'
    Continue = 'continue'
    Complete = 'complete'

    @classmethod
    def validate_change_status(cls, status):
        return status in [cls.Start.value, cls.Pause.value, cls.Continue.value, cls.Complete.value]
