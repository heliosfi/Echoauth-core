from src.authority.models import AuthorityRecord
from src.authority.registry import AuthorityRegistry


def test_registry_registration():

    registry = AuthorityRegistry()

    record = AuthorityRecord(
        authority_id="AUTH-001",
        owner_id="PARENT-001",
        authority_type="parent"
    )

    registry.register(record)

    assert registry.exists("AUTH-001")