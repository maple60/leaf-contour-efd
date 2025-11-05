# pyi_rth_torchpath.py
import os
import sys


def _add(path: str):
    if os.path.isdir(path):
        try:
            os.add_dll_directory(path)
        except Exception:
            pass


if getattr(sys, "frozen", False):
    print("Running torchpath runtime hook...")
    # --- 安全にベースディレクトリを決定 ---
    if hasattr(sys, "_MEIPASS") and os.path.exists(sys._MEIPASS):
        # onefile 実行時
        base = sys._MEIPASS
        print("Detected _MEIPASS for onefile execution.")
        print(f"Determined base directory: {base}")
    else:
        # onedir 実行時
        base = os.path.dirname(sys.executable)
        print("Detected onedir execution.")
        print(f"Determined base directory: {base}")

    torch_candidates = [
        os.path.join(base, "torch", "lib"),
        os.path.join(base, "_internal", "torch", "lib"),
        os.path.join(base, "torch"),
        os.path.join(base, "_internal", "torch"),
    ]

    for path in torch_candidates:
        _add(path)

    # PATH を更新
    env_path = ";".join(torch_candidates) + ";" + os.environ.get("PATH", "")
    os.environ["PATH"] = env_path

    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

# runtime hook の末尾に追加
print("DLL search order:")
for p in torch_candidates:
    print(" -", p, "=>", os.path.exists(os.path.join(p, "c10.dll")))
