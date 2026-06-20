from .registry import AuthorityRegistry


class AuthorityValidator:
    """
    Validates authority ownership and delegation chains.
    """

    def __init__(self, registry: AuthorityRegistry):
        self.registry = registry

    def validate_authority(self, authority_id: str) -> bool:
        return self.registry.exists(authority_id)

    def validate_delegation(
        self,
        parent_authority: str,
        delegated_authority: str
    ) -> bool:

        parent = self.registry.get(parent_authority)
        child = self.registry.get(delegated_authority)

        if not parent:
            return False

        if not child:
            return False

        return child.parent_authority == parent.authority_id
