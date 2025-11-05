# https://github.com/pyinstaller/pyinstaller/issues/8966
# hook-sam2.py
# Custom hook to include SAM2 package correctly in PyInstaller builds
# SAM2 has a nested "sam2/sam2" structure, so we need to flatten it.

"""
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("sam2")

# datas = collect_data_files("sam2")
# hiddenimports = collect_submodules("sam2")
module_collection_mode = "pyz+py"
"""

import os
from PyInstaller.utils.hooks import collect_submodules

datas = []
binaries = []
hiddenimports = []

# --- ルートディレクトリを明示的に指定 ---
project_root = os.getcwd()
inner_sam2_path = os.path.join(project_root, "sam2", "sam2")  # 実パッケージの場所

# --- sam2/sam2 ディレクトリを "sam2" としてコピーする ---
if os.path.isdir(inner_sam2_path):
    for root, _, files in os.walk(inner_sam2_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, inner_sam2_path)
            target_path = os.path.join("sam2", rel_path)  # 出力先: _internal/sam2/...
            datas.append((full_path, target_path))

# --- モジュールを明示的に列挙して import 対象にする ---
hiddenimports += collect_submodules("sam2.sam2")

module_collection_mode = "pyz+py"
