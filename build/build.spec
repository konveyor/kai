# -*- mode: python ; coding: utf-8 -*-

# This is a PyInstaller build spec to build Kai Client into a binary
# To run this spec, activate Kai venv and run `pyinstaller ./build.spec`

import sys
import os
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_data_files

#data_dirs = [
#    ('../data/templates', 'data/templates'),
#]

script_path = '../kai/rpc_server/main.py'

a = Analysis(
    [script_path],
    pathex=[os.path.dirname(script_path), '../'],
    binaries=[],
#    datas=data_dirs,
    hiddenimports=["_ssl"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    # cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="kai-rpc-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

