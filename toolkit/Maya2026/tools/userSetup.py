from maya import cmds

cmds.evalDeferred(
    "from tapipeline_bootstrap import bootstrap; bootstrap.run()",
    lowestPriority=True,
)
