from __future__ import annotations

import os

from . import logger

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5678

_listening = False
_endpoint: tuple[str, int] | None = None


def _mayapy_path() -> str:
    maya_location = os.environ.get("MAYA_LOCATION", "")
    if not maya_location:
        raise RuntimeError(
            "MAYA_LOCATION not set; launch Maya via launch.bat "
            "so config/maya2026_env.ini is exported."
        )
    mayapy = os.path.join(maya_location, "bin", "mayapy.exe")
    if not os.path.exists(mayapy):
        raise RuntimeError(f"mayapy.exe not found at {mayapy}")
    return mayapy


def enable(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> tuple[str, int]:
    global _listening, _endpoint
    log = logger.get_logger()

    if _listening and _endpoint is not None:
        log.info("debugpy already listening on %s:%d", *_endpoint)
        return _endpoint

    os.environ.setdefault("PYDEVD_DISABLE_FILE_VALIDATION", "1")

    import debugpy

    debugpy.configure(python=_mayapy_path())
    debugpy.listen((host, port))

    _listening = True
    _endpoint = (host, port)
    log.info("debugpy listening on %s:%d (attach from VSCode)", host, port)
    return _endpoint


def is_listening() -> bool:
    return _listening


def endpoint() -> tuple[str, int] | None:
    return _endpoint
