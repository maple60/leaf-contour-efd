# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_all, collect_dynamic_libs
from PyInstaller.building.build_main import Tree
import glob
import sys
import os
import torch

datas = []
binaries = []
hiddenimports = []

# --- Add torch package data and binaries ---
torch_dir = os.path.dirname(torch.__file__)
torch_tree = Tree(torch_dir, prefix="torch")  # copy entire torch directory
binaries += collect_dynamic_libs("torch")
hiddenimports += ["torch", "torch._C", "torchvision"]

# --- Add Visual C++ runtime DLLs manually ---
system32 = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32")

# find required VC runtime DLLs
vcruntime_dlls = [
    "vcruntime140.dll",
    "vcruntime140_1.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
]

for dll in vcruntime_dlls:
    src = os.path.join(system32, dll)
    if os.path.exists(src):
        binaries.append((src, "."))

# Collect from core dependencies
for pkg in ["PyQt6", 
    "napari", 
    "napari_builtins", 
    "vispy", 
    "magicgui", 
    "imageio", 
    "PIL", 
    "tifffile", 
    "torch", 
    "torchvision", 
    "pywin32-ctypes",
    ]:
    tmp = collect_all(pkg)
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

# Also include MSVC-dependent dynamic libraries for torch
binaries += collect_dynamic_libs("torch")

# Additional hidden imports for readers
hiddenimports += [
    "imageio.plugins.pillow",
    "imageio.plugins.tifffile",
    "PIL.JpegImagePlugin",
    "PIL.PngImagePlugin",
    "PIL.TiffImagePlugin",
    "PIL.BmpImagePlugin",
    "napari_builtins",  # built-in readers
]

# --- Napari plugins ---
hiddenimports += collect_submodules('napari.plugins')
hiddenimports += collect_submodules('napari.plugins.io')
hiddenimports += collect_submodules('napari.plugins._builtins')

# Safety: ensure all imageio plugins are bundled
hiddenimports += collect_submodules('imageio.plugins')

# --- Add SAM2 if exists locally ---
sam2_path = os.path.join(os.getcwd(), "sam2")
if os.path.isdir(sam2_path):
    datas += [(sam2_path, "sam2")]  # include the entire sam2 directory
    hiddenimports += collect_submodules("sam2")

a = Analysis(
    ['src\\leaf_shape_tool\\__main__.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=["extra_hooks\\hook-sam2.py"],
    hooksconfig={},
    runtime_hooks=["runtime_hooks\\pyi_rth_torchpath.py"],
    excludes=[
        "OpenGL",
        "torch.distributed",
        "torch.testing",
        "torch.distributed.elastic",
    ],
    noarchive=False,
    optimize=0,
)

a.datas += torch_tree # Add the torch Tree AFTER Analysis
pyz = PYZ(a.pure) # Build EXE

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LeafShapeTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='LeafShapeTool'
)
