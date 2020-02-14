"""
  TESTING DATABASE CONSTANTS
"""

# CAMERAS
TEST_EXPERIMENTS_USER = 'victor'
TEST_EXPERIMENTS_CAMERAS = [
    {
        'user': TEST_EXPERIMENTS_USER,
        'name': 'test',
        'ip': '111.11.11.11',
    },
    {
        'user': TEST_EXPERIMENTS_USER,
        'name': 'test2',
        'ip': '777.11.11.77',
        'place': 'moscow',
    },
]

TEST_EXPERIMENTS_EXPERIMENT = {
        'user': TEST_EXPERIMENTS_USER,
        'title': 'test',
        'description': 'test...',
}

TEST_EXPERIMENTS_MOUSE = {
        'user': TEST_EXPERIMENTS_USER,
        'name': 'pinky',
}

TEST_EXPERIMENTS_CREATE_EXPERIMENT = {
        'user': TEST_EXPERIMENTS_USER,
        'title': 'test2',
        'description': 'test2...',
}

TEST_EXPERIMENTS_CHANGE_FIELDS = {
    'title': 'test555',
}
