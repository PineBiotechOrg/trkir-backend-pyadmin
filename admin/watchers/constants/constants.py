import os
from enum import Enum
from kafka import KafkaProducer


DECODE_FORMAT = 'utf-8'

# Списком через "," перечислять
KAFKA_SERVERS = os.getenv('TRKIR_KAFKA_SERVERS').split(',')

try:
    PRODUCER = KafkaProducer(
        bootstrap_servers=KAFKA_SERVERS
    )
except Exception:
    # TODO: logging no producer (and reload it somehow) https://tracker.yandex.ru/VPAGROUPDEV-907
    #  None - for future checks
    PRODUCER = None


class Topics(Enum):
    ExperimentManager = 'experiment_manager'


class ExperimentWatcherRequests(Enum):
    Create = 'create'
    Remove = 'remove'
    Update = 'update'
