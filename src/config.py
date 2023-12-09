import platform
import shutil
import json
from pathlib import Path
from enum import Enum


def get_config_dir() -> Path:
    home = Path.home()
    if (pl := platform.system()) == "Windows":
        confp = home.joinpath(r"AppData\Roaming\dwt")
    elif pl == "Darwin":
        confp = home.joinpath("Library/Preferences/dwt")
    else:
        confp = home.joinpath(".config/dwt")
    return confp


def is_exists_config():
    _dir = get_config_dir()
    if not _dir.exists():
        return False
    if not _dir.joinpath("config.json").exists():
        return False
    return True


def create_config(force=False):
    _dir = get_config_dir()
    if is_exists_config():
        if not force:
            return False
        shutil.rmtree(_dir, True)
    _dir.mkdir()

    conf = _dir.joinpath("config.json")
    conf.touch()
    conf.write_text("{}")

    users = _dir.joinpath("users.json")
    DEFAULT_USER = {
        "youtube": [],
        "spotify": []
    }
    users.touch()
    users.write_text(json.dumps(DEFAULT_USER, indent=4))
    return True


class Streamer(Enum):
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"


class Config:
    def __init__(self):
        self.dir_path = get_config_dir()
        self.config_json_path = self.dir_path.joinpath("config.json")
        self.users_json_path = self.dir_path.joinpath("users.json")
        self.created_status = create_config()

    def load(self):
        self._config_json = json.loads(self.config_json_path.read_text("utf8"))
        self._users_json = json.loads(self.users_json_path.read_text("utf8"))

    @property
    def config(self):
        if hasattr(self, "_config_json"):
            return self._config_json
        self.load()
        return self._config_json

    @property
    def credentials(self):
        if hasattr(self, "_users_json"):
            return self._users_json
        self.load()
        return self._users_json

    def default_user(self, type: Streamer):
        f = list(filter(lambda x: x["default"], self.credentials[type.value]))
        if not f:
            return None
        return f[0]

    def add_user(self, username, password, type: Streamer, default: bool = False):
        data = self.credentials
        data[type.value].append({"username": username, "password": password, "default": default})
        self.users_json_path.write_text(json.dumps(data, indent=4), "utf8")
