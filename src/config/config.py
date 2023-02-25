from configparser import ConfigParser
from pathlib import Path

# get absolute path to database.ini
current_path = Path(__file__).absolute()
db_config = current_path.parent.joinpath("database.ini")


def parse_config(filename=db_config, section="postgresql"):
    """return parsed database config as dictionary"""

    parser = ConfigParser()  # create a parser
    parser.read(filename)  # read config file

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db
