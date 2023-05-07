from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Element:
    text: Optional[str]
    attr: Optional[Dict[str, str]]
    parent: Optional[Any]
