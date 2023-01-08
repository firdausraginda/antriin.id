import random, string


def convert_model_to_dict(query_result) -> dict:
    """convert sqlalchemy model to dictionary"""

    key = [
        getattr(query_result, column.name) for column in query_result.__table__.columns
    ]
    value = [column.key for column in query_result.__table__.columns]

    return dict(zip(value, key))


def generate_short_url() -> str:

    return "".join(random.choices(string.ascii_letters, k=5))
