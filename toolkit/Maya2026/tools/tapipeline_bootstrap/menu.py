from maya import cmds, mel

from . import logger

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
        label="Reload Bootstrap",
        parent=menu,
        command=lambda *_: _reload(),
    )

    log.info("Top menu '%s' created", MENU_LABEL)
    return menu


def _reload() -> None:
    import importlib
    from . import bootstrap as _bootstrap

    importlib.reload(_bootstrap)
    _bootstrap.run()
