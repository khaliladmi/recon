from plugins.base import BasePlugin
import subprocess

class Plugin(BasePlugin):
    name = "echo"
    mode = "passive"

    def run(self, target: str) -> str:
        proc = subprocess.run(["echo", target], capture_output=True, text=True)
        return proc.stdout.strip()

