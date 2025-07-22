class BasePlugin:
    name = "base"
    mode = "passive"  # or 'active'

    def run(self, target: str) -> str:
        raise NotImplementedError

