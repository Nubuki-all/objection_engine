import threading

class _Config(threading.local):
    def __init__(self):
        self.assets_folder = "assets"

_config = _Config()

def get_assets_folder():
    return _config.assets_folder

def set_assets_folder(path):
    _config.assets_folder = path

class assets_context:
    def __init__(self, assets_folder):
        self.new_folder = assets_folder
        self.old_folder = get_assets_folder()

    def __enter__(self):
        set_assets_folder(self.new_folder)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_assets_folder(self.old_folder)
