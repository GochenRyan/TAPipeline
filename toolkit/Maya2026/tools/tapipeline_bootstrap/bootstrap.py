from . import logger, menu


def run() -> None:
    log = logger.init()
    log.info("Bootstrap starting")
    try:
        menu.create()
    except Exception:
        log.exception("Failed to create TAPipeline menu")
        return
    log.info("Bootstrap completed")
