# TAPipeline

Maya 2026 TA pipeline: Python tools, future C++ plug-ins, sample scenes and configuration.

## Quick start

1. Edit `MAYA_LOCATION` in [config/maya2026_env.ini](config/maya2026_env.ini) to point at your Maya 2026 install (the folder that contains `bin\maya.exe`).
2. Double-click [launch.bat](launch.bat).
   - On first launch the script installs every dependency listed in [toolkit/Maya2026/requirements.txt](toolkit/Maya2026/requirements.txt) into `toolkit/Maya2026/python/3.11/`. Subsequent launches re-sync to pick up new entries.
   - Maya boots with `MAYA_MODULE_PATH` pointed at `toolkit/Maya2026/`, so `TAPipeline.mod` is loaded automatically.
3. After Maya finishes loading you should see a **TAPipeline** menu in the top menubar and a launch entry in `%USERPROFILE%\Documents\maya\2026\logs\tapipeline_YYYYMMDD.log`.

## Repository layout

```
TAPipeline/
├── launch.bat                            # Reads ini, syncs deps, starts Maya
├── config/
│   └── maya2026_env.ini                  # MAYA_LOCATION lives here
├── plugins/                              # (planned) C++ source + CMake
└── toolkit/
    └── Maya2026/
        ├── TAPipeline.mod                # Injects paths into Maya
        ├── requirements.txt              # Third-party Python deps
        ├── plug-ins/                     # Compiled .mll output
        ├── icons/                        # Menu / shelf icons
        ├── shelves/                      # shelf_TAPipeline.mel (planned)
        ├── samples/scenes/               # Test .ma / .mb scenes
        ├── python/3.11/                  # pip-installed deps (gitignored)
        └── tools/
            ├── userSetup.py              # Auto-loaded by Maya, schedules bootstrap
            └── tapipeline_bootstrap/     # logger / menu / bootstrap entry
```

## How the boot chain works

1. `launch.bat` parses `config/maya2026_env.ini` (KEY=VALUE, `#` for comments) and exports every entry as an environment variable.
2. `MAYA_MODULE_PATH` is set to `toolkit/Maya2026/`, where Maya finds `TAPipeline.mod`.
3. `TAPipeline.mod` adds `python/3.11/` and `tools/` to `PYTHONPATH`, plus `plug-ins/`, `icons/`, `shelves/` to their respective Maya search paths.
4. Maya auto-imports `tools/userSetup.py`, which uses `evalDeferred` to call `tapipeline_bootstrap.bootstrap.run()` once the main window exists.
5. `bootstrap.run()` initializes the rotating log file and creates the top-level menu.

## Adding a Python dependency

1. Edit `toolkit/Maya2026/requirements.txt`.
2. Re-run `launch.bat`. The pip install step is idempotent and `--upgrade` will pick up the new package.

## Adding a Python tool

1. Drop your package or module under `toolkit/Maya2026/tools/`.
2. Wire its entry point into `tapipeline_bootstrap/menu.py` so it shows up in the **TAPipeline** menu.

## Adding a C++ plug-in (planned, M4)

1. Add source under `plugins/<plugin_name>/`.
2. CMake `install()` copies the `.mll` into `toolkit/Maya2026/plug-ins/`.
3. Maya's Plug-in Manager picks it up via `MAYA_PLUG_IN_PATH` from `TAPipeline.mod`.

## Troubleshooting

- **No TAPipeline menu**: open the Script Editor and check for tracebacks. Verify `MAYA_MODULE_PATH` points at `toolkit/Maya2026/` (run `import os; print(os.environ["MAYA_MODULE_PATH"])`).
- **`ImportError: tapipeline_bootstrap`**: confirm `tools/` is in `sys.path`. Print `sys.path` in the Script Editor; the `tools/` folder should be there courtesy of `TAPipeline.mod`.
- **Dependency install fails**: rerun `launch.bat` from a `cmd` window so the `pip` output stays visible, or run the `mayapy -m pip install` line manually.
