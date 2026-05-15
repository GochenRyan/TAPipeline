if __name__ == "__main__":
    import maya.cmds as cmds
    import maya.mel as mel

    # Load the userSetup script
    try:
        cmds.evalDeferred("import userSetup_2026")
        print("userSetup_2026.py loaded successfully.")
    except Exception as e:
        print(f"Error loading userSetup_2026.py: {e}")