from maya import cmds, mel

from . import debug, logger

MENU_NAME = "TAPipelineMenu"
MENU_LABEL = "TAPipeline"


def _main_window() -> str:
    return mel.eval("$tmp = $gMainWindow")


def remove() -> None:
    if cmds.menu(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME, menu=True)


def create() -> str:
    log = logger.get_logger()
    remove()

    menu = cmds.menu(
        MENU_NAME,
        label=MENU_LABEL,
        parent=_main_window(),
        tearOff=True,
    )

    cmds.menuItem(
        label="Hello PySide6",
        parent=menu,
        command=lambda *_: __import__("hello_pyside").show(),
    )

    cmds.menuItem(
        label="About TAPipeline...",
        parent=menu,
        command=lambda *_: cmds.confirmDialog(
            title="TAPipeline",
            message="TAPipeline for Maya 2026\nBootstrap loaded.",
            button=["OK"],
        ),
    )
    cmds.menuItem(divider=True, parent=menu)
    cmds.menuItem(
        label="Enable Debugpy (5678)",
        parent=menu,
        command=lambda *_: _enable_debugpy(),
    )
    cmds.menuItem(
        label="Reload Bootstrap",
        parent=menu,
        command=lambda *_: _reload(),
    )

    log.info("Top menu '%s' created", MENU_LABEL)
    return menu


def _enable_debugpy() -> None:
    log = logger.get_logger()
    try:
        host, port = debug.enable()
    except Exception as exc:
        log.exception("Failed to enable debugpy")
        cmds.confirmDialog(
            title="TAPipeline — Debugpy",
            message=f"Failed to enable debugpy:\n\n{exc}",
            button=["OK"],
            icon="critical",
        )
        return

    cmds.confirmDialog(
        title="TAPipeline — Debugpy",
        message=(
            f"debugpy listening on {host}:{port}\n\n"
            "In VSCode: Run and Debug → Attach Maya."
        ),
        button=["OK"],
    )


def _reload() -> None:
    import importlib
    import sys

    pkg = __package__  # "tapipeline_bootstrap"
    names = [
        n for n in list(sys.modules)
        if n == pkg or n.startswith(pkg + ".")
    ]
    # First, reload the sub-modules (those with more points should be loaded first), and finally reload the package itself.
    for name in sorted(names, key=lambda n: n.count("."), reverse=True):
        importlib.reload(sys.modules[name])

    from . import bootstrap as _bootstrap
    _bootstrap.run()
