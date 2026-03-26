# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_all, collect_dynamic_libs
from PyInstaller.building.build_main import Tree
import os
import platform
import torch

is_windows = platform.system() == "Windows"

datas = []
binaries = []
hiddenimports = []

# --- Add torch package data and binaries ---
torch_dir = os.path.dirname(torch.__file__)
torch_tree = Tree(torch_dir, prefix="torch")
binaries += collect_dynamic_libs("torch")
hiddenimports += ["torch", "torch._C", "torchvision"]

# --- Windows-only Visual C++ runtime DLLs ---
if is_windows:
    system32 = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32")
    vcruntime_dlls = [
        "vcruntime140.dll",
        "vcruntime140_1.dll",
        "msvcp140.dll",
        "msvcp140_1.dll",
        "msvcp140_atomic_wait.dll",
        "concrt140.dll",
        "libiomp5md.dll",
    ]

    for dll in vcruntime_dlls:
        src = os.path.join(system32, dll)
        if os.path.exists(src):
            binaries.append((src, "."))

# Collect from core dependencies
for pkg in [
    "PyQt6",
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
    try:
        tmp = collect_all(pkg)
        datas += tmp[0]
        binaries += tmp[1]
        hiddenimports += tmp[2]
    except Exception:
        # Skip optional/platform-specific package collection.
        pass

# Additional hidden imports for readers and SAM2 dependencies
hiddenimports += [
    "imageio.plugins.pillow",
    "imageio.plugins.tifffile",
    "PIL.JpegImagePlugin",
    "PIL.PngImagePlugin",
    "PIL.TiffImagePlugin",
    "PIL.BmpImagePlugin",
    "napari_builtins",
    "hydra",
    "iopath",
]

hiddenimports += collect_submodules("napari.plugins")
hiddenimports += collect_submodules("napari.plugins.io")
hiddenimports += collect_submodules("napari.plugins._builtins")
hiddenimports += collect_submodules("imageio.plugins")

# --- Add local SAM2 if exists ---
sam2_path = os.path.join(os.getcwd(), "sam2", "sam2")
if os.path.isdir(sam2_path):
    datas += [(sam2_path, "sam2")]
    hiddenimports += collect_submodules("sam2")

runtime_hooks = [
    os.path.join("runtime_hooks", "pyi_rth_disable_torchjit.py"),
    os.path.join("runtime_hooks", "pyi_rth_torchpath.py"),
]

a = Analysis(
    [os.path.join("src", "leaf_shape_tool", "__main__.py")],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[os.path.join("extra_hooks", "hook-sam2.py")],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=[
        "OpenGL",
        "torch.distributed",
        "torch.testing",
        "torch.distributed.elastic",
    ],
    noarchive=False,
    optimize=0,
)

a.datas += torch_tree
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LeafShapeTool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="LeafShapeTool",
)
