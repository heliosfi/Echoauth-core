from .models import AuthorityRecord


class AuthorityRegistry:
    """
    Central registry for authority ownership.
    """

    def __init__(self):
        self._registry = {}

    def register(self, record: AuthorityRecord):
        self._registry[record.authority_id] = record

    def get(self, authority_id: str):
        return self._registry.get(authority_id)

    def exists(self, authority_id: str) -> bool:
        return authority_id in self._registry