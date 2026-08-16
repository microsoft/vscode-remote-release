from ._importlib import metadata

try:
    __version__ = metadata.version('setuptools') or '0.dev0+unknown'
except Exception:  # noqa: BLE001 # intentional broad fallback
    __version__ = '0.dev0+unknown'
