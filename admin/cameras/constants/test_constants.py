"""
  TESTING DATABASE CONSTANTS
"""
import datetime


# CAMERAS
TEST_CAMERAS_USER = 'victor'
TEST_CAMERAS_CAMERA = [
    {
        'user': TEST_CAMERAS_USER,
        'name': 'test',
        'ip': '111.11.11.11',
        'date_added': datetime.datetime.now(),
    },
    {
        'user': TEST_CAMERAS_USER,
        'name': 'test2',
        'ip': '777.11.11.77',
        'date_added': datetime.datetime.now(),
        'place': 'moscow',
    },
]

TEST_CAMERAS_CREATE_CAMERA = {
    'user': TEST_CAMERAS_USER,
    'camera': {
        'name': 'test3',
        'ip': '777.11.77.77',
        'place': 'moscow',
    }
}

TEST_CAMERAS_CHANGE_FIELDS = {
    'ip': '222.22.22.33',
}
