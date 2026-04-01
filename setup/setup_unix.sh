# Usage:
# chmod +x setup_unix.sh
# ./setup_unix.sh

#!/usr/bin/env bash
set -e

# === Move to script directory ===
cd "$(dirname "$0")/.."

# === Step 1: Create or activate virtual environment ===
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
fi

source .venv/bin/activate

# === Step 2: Sync project dependencies ===
echo "Syncing environment..."
uv sync

# === Step 3: Ensure SAM2 exists ===
if [ ! -d "sam2" ]; then
    echo "SAM2 not found. Cloning from GitHub..."
    git clone https://github.com/facebookresearch/sam2.git || {
        echo "[Error] Git clone failed."
        exit 1
    }
fi

# === Step 4: Install SAM2 in editable mode ===
if [ -d "sam2" ]; then
    echo "Installing SAM2 in editable mode..."
    cd sam2
    uv pip install -e .
    cd ..
else
    echo "[Warning] sam2 directory not found."
fi

# === Step 5: Ensure SAM2 checkpoints exist ===
if [ -d "sam2/checkpoints" ]; then
    echo "Checking SAM2 checkpoints..."
    check_download "sam2/checkpoints" || echo "[Warning] Failed to download checkpoints."
else
    echo "[Info] sam2/checkpoints directory not found."
fi

# === Step 6: Run the LeafContourEFD ===
echo "Launching LeafContourEFD..."
leaf-contour-efd

# =========================
# Functions
# =========================

check_download() {
    CKPT_DIR="$1"
    cd "$CKPT_DIR"

    BASE_URL="https://dl.fbaipublicfiles.com/segment_anything_2/092824"

    download_if_missing "sam2.1_hiera_tiny.pt"      "$BASE_URL/sam2.1_hiera_tiny.pt"
    download_if_missing "sam2.1_hiera_small.pt"     "$BASE_URL/sam2.1_hiera_small.pt"
    download_if_missing "sam2.1_hiera_base_plus.pt" "$BASE_URL/sam2.1_hiera_base_plus.pt"
    download_if_missing "sam2.1_hiera_large.pt"     "$BASE_URL/sam2.1_hiera_large.pt"

    cd - > /dev/null
}

download_if_missing() {
    FILE="$1"
    URL="$2"

    if [ -f "$FILE" ]; then
        echo "[Skip] $FILE already exists."
    else
        echo "[Download] $FILE"
        if command -v curl >/dev/null 2>&1; then
            curl -L -o "$FILE" "$URL"
        elif command -v wget >/dev/null 2>&1; then
            wget -O "$FILE" "$URL"
        else
            echo "[Error] curl or wget not found."
            return 1
        fi
    fi
}
