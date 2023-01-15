import random, string


def convert_model_to_dict(query_result) -> dict:
    """convert sqlalchemy model to dictionary"""

    key = [
        getattr(query_result, column.name) for column in query_result.__table__.columns
    ]
    value = [column.key for column in query_result.__table__.columns]

    return dict(zip(value, key))


def generate_short_url() -> str:
    """generate 5 random string as short_url"""

    return "".join(random.choices(string.ascii_letters, k=5))


def update_existing_data(existing_data, body_data: dict) -> None:
    """update existing data with value in body request"""

    [setattr(existing_data, key, val) for key, val in body_data.items()]

    return None
