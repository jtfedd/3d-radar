import uuid as uuid_gen


def uuid() -> str:
    return uuid_gen.uuid4().hex
