from datetime import datetime


def serialize_model(obj):

    data = {}

    for column in obj.__table__.columns:
        value = getattr(obj, column.name)

        if isinstance(value, datetime):
            value = value.isoformat()

        data[column.name] = value

    return data
