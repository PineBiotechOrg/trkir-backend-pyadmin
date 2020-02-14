from watchers.constants.constants import \
    PRODUCER, \
    DECODE_FORMAT, \
    Topics


class WatcherRequests:
    @staticmethod
    def manage_experiment_watcher(experiment_id, status):
        # TODO logging https://tracker.yandex.ru/VPAGROUPDEV-907
        PRODUCER.send(
            Topics.ExperimentManager.value,
            key=experiment_id.encode(DECODE_FORMAT),
            value=status.encode(DECODE_FORMAT),
        )
