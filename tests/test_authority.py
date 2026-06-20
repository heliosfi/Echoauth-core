from echoauth.authority.models import AuthorityRecord
from echoauth.authority.registry import AuthorityRegistry


def test_registry_registration():

    registry = AuthorityRegistry()

    record = AuthorityRecord(
        authority_id="AUTH-001",
        owner_id="PARENT-001",
        authority_type="parent"
    )

    registry.register(record)

    assert registry.exists("AUTH-001")
