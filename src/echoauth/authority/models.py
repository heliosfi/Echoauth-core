from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthorityRecord:
    authority_id: str
    owner_id: str
    authority_type: str
    parent_authority: Optional[str] = None
    active: bool = True
