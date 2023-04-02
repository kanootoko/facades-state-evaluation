"""
All FastApi endpoints are exported from this module.
"""
import importlib
from pathlib import Path
from facades_api.endpoints.routers import list_of_routers

for file in sorted(Path(__file__).resolve().parent.iterdir()):
    if file.name.endswith(".py") and file.name not in ("__init__.py", "router.py"):
        importlib.import_module(f".{file.name[:-3]}", __package__)

__all__ = [
    "list_of_routers",
]
