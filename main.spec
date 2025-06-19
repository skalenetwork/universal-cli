# -*- mode: python -*-

# import distutils
# if distutils.distutils_path.endswith('__init__.py'):
#    distutils.distutils_path = os.path.dirname(distutils.distutils_path)


import importlib
import os
import sys

package_imports = [['sgx', ['generate.sh']]]

external_data = []

for package, files in package_imports:
    proot = os.path.dirname(importlib.import_module(package).__file__)
    external_data.extend((os.path.join(proot, f), package) for f in files)


block_cipher = None
binaries = ()
runtime_hooks = ()
hookspath = () 


a = Analysis(
    ['./main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=[
        *external_data
    ],
    hiddenimports=[
        'eth_hash.pkg_resources.pysha3', 
        'pkg_resources.py2_warn', 
        'cmath'
    ],
    hookspath=hookspath,
    runtime_hooks=runtime_hooks,
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True 
)
