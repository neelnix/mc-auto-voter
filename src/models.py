from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


@dataclass
class AutomationResult:
    domain: str
    vote: Status
    operation: Status
    logs: list[str] = field(default_factory=list)
