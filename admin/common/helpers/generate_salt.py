import uuid


def generate_salt():
    return uuid.uuid4().hex
