from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent
_SOURCE_PACKAGE_DIR = _PACKAGE_DIR.parent / "source" / "tracker_app"

__path__ = [str(_PACKAGE_DIR)]

if _SOURCE_PACKAGE_DIR.is_dir():
    __path__.append(str(_SOURCE_PACKAGE_DIR))
