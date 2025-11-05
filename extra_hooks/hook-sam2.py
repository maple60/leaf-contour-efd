# https://github.com/pyinstaller/pyinstaller/issues/8966
# hook-sam2.py
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("sam2")

# datas = collect_data_files("sam2")
# hiddenimports = collect_submodules("sam2")
module_collection_mode = "pyz+py"
