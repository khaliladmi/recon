import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type

from plugins.base import BasePlugin

BUILTIN_PATH = Path(__file__).resolve().parent.parent / "plugins" / "builtin"
EXTERNAL_PATH = Path(__file__).resolve().parent.parent / "plugins" / "external"


def load_plugins() -> Dict[str, Type[BasePlugin]]:
    plugins = {}
    for path in [BUILTIN_PATH, EXTERNAL_PATH]:
        for _, name, _ in pkgutil.iter_modules([str(path)]):
            module = importlib.import_module(f"plugins.{path.name}.{name}")
            if hasattr(module, "Plugin"):
                plugin_cls = getattr(module, "Plugin")
                if issubclass(plugin_cls, BasePlugin):
                    plugins[plugin_cls.name] = plugin_cls
    return plugins

