import os
from .config import get_assets_folder

class AssetsFolder:
    def __str__(self):
        return str(get_assets_folder())

    def __repr__(self):
        return repr(get_assets_folder())

    def __fspath__(self):
        return str(get_assets_folder())

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __getattr__(self, name):
        return getattr(str(self), name)
