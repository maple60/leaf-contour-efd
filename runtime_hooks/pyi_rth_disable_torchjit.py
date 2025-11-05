# runtime_hooks/pyi_rth_disable_torchjit.py
import os
# JIT 全体を無効化
os.environ["PYTORCH_JIT"] = "0"

# 念のための保険（scriptを素通りに）
try:
    import torch
    def _no_script(x, *a, **k):
        return x
    torch.jit.script = _no_script
except Exception:
    pass
