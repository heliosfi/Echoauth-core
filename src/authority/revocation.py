from .registry import AuthorityRegistry


class AuthorityRevocation:

    def __init__(self, registry: AuthorityRegistry):
        self.registry = registry

    def revoke(self, authority_id: str) -> bool:

        record = self.registry.get(authority_id)

        if not record:
            return False

        record.active = False
        return True