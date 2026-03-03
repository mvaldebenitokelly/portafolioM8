import os
import zipfile
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

EXCLUDE_DIRS = {"venv", "__pycache__", ".git","media"}

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
zip_name = f"{PROJECT_NAME}_{timestamp}.zip"
zip_path = os.path.join(PROJECT_ROOT, zip_name)

def should_exclude(path):
    return any(part in EXCLUDE_DIRS for part in path.split(os.sep))

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.endswith(".zip"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)

            if not should_exclude(rel_path):
                zipf.write(full_path, rel_path)

print(f"Compresión de carpetas realizadas correctamente: {zip_name}")
