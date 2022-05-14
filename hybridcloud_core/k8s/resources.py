from dataclasses import dataclass
from enum import Enum


class Scope(Enum):
    NAMESPACED = "namespaced"
    CLUSTER = "cluster"


@dataclass
class Resource:
    group: str
    version: str
    plural: str
    kind: str
    scope: Scope

    def kopf_on(self):
        return [self.group, self.version, self.plural]
