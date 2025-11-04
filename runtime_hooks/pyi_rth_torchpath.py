# pyi_rth_torchpath.py
# Ensure torch DLLs are found in PyInstaller onefile builds
# （日英併記コメント / JP-EN comments）
import os, sys

def _add(path: str):
    if os.path.isdir(path):
        try:
            os.add_dll_directory(path)
        except Exception:
            pass

if getattr(sys, "frozen", False):
    base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

    # --- search possible torch locations ---
    torch_candidates = [
        os.path.join(base, "torch", "lib"),
        os.path.join(base, "_internal", "torch", "lib"),
        os.path.join(base, "torch"),
        os.path.join(base, "_internal", "torch"),
    ]

    for path in torch_candidates:
        _add(path)

    # PATH環境変数も拡張してDLL探索を確実化
    env_path = ";".join(torch_candidates) + ";" + os.environ.get("PATH", "")
    os.environ["PATH"] = env_path

    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
