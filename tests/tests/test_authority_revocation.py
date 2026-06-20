from src.authority.models import AuthorityRecord
from src.authority.registry import AuthorityRegistry
from src.authority.revocation import AuthorityRevocation


def test_authority_revocation():

    registry = AuthorityRegistry()

    record = AuthorityRecord(
        authority_id="AUTH-001",
        owner_id="PARENT-001",
        authority_type="parent"
    )

    registry.register(record)

    revocation = AuthorityRevocation(registry)

    assert revocation.revoke("AUTH-001")

    assert registry.get("AUTH-001").active is False