from dataclasses import dataclass

@dataclass
class ActionResult:
    terminal: bool = False
    win: bool = False